from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from datetime import datetime
from .models import Building, Room, Reservation, Member

# -------------------
# HOME PAGE
# -------------------
def home(request):
    buildings = Building.objects.all()

    # Search
    search = request.GET.get('search', '')
    if search:
        buildings = buildings.filter(name__icontains=search) | buildings.filter(campus__icontains=search)

    # Campus filter
    campus = request.GET.get('campus', '')
    if campus and campus != 'All Campuses':
        buildings = buildings.filter(campus=campus)

    # Available Now filter
    available = request.GET.get('available', '')
    if available:
        buildings = buildings.filter(room__available=True).distinct()


    return render(request, 'testApp/home.html', {
        'buildings': buildings,
        'search': search,
        'campus': campus,
    })

# -------------------
# LOGIN
# -------------------
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error = "Invalid credentials. Please use your UTRGV username and password."
    return render(request, 'testApp/login.html', {"error": error})

def logout_view(request):
    logout(request)
    return redirect("login")

def signup_view(request):
    return redirect("login")

# -------------------
# ABOUT / CONTACT / MEMBERS
# -------------------
def about(request):
    template = loader.get_template('testApp/about.html')
    return HttpResponse(template.render())

def contact(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('testApp/contact.html')
    context = {'mymembers': mymembers}
    return HttpResponse(template.render(context, request))

def details(request, id):
    mymember = Member.objects.get(id=id)
    template = loader.get_template('testApp/details.html')
    context = {'mymember': mymember}
    return HttpResponse(template.render(context, request))

# -------------------
# STEP 1 - SELECT ROOM
# -------------------
def select_room_view(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    rooms = Room.objects.filter(building=building)
    seat_filter = request.GET.get('seats')
    if seat_filter:
        rooms = rooms.filter(seating__gte=seat_filter)
    return render(request, 'testApp/select_room.html', {
        'building': building,
        'rooms': rooms
    })

# -------------------
# STEP 2 - TIME SELECTION + BOOKING
# -------------------
def time_select_view(request, room_id):
    if not request.user.is_authenticated:
        return redirect("login")

    room = get_object_or_404(Room, id=room_id)
    time_slots = list(range(8, 18))

    # Get selected date or default to today
    selected_date_str = request.GET.get('date', '') or request.POST.get('date', '')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = datetime.now().date()
    else:
        selected_date = datetime.now().date()

    # Get booked hours for this room on the selected date
    reservations = Reservation.objects.filter(
        room=room,
        start_time__date=selected_date
    )
    booked_hours = []
    for r in reservations:
        start = r.start_time.hour
        end = r.end_time.hour
        for h in range(start, end):
            booked_hours.append(h)
    booked_hours = list(set(booked_hours))

    if request.method == "POST":
        start_hour = int(request.POST.get("start_time"))
        end_hour = int(request.POST.get("end_time"))

        for h in range(start_hour, end_hour):
            if h in booked_hours:
                return render(request, "testApp/time_select.html", {
                    "room": room,
                    "time_slots": time_slots,
                    "booked_hours": booked_hours,
                    "selected_date": selected_date,
                    "error": "That time is already booked!"
                })

        start_datetime = datetime.combine(selected_date, datetime.min.time().replace(hour=start_hour))
        end_datetime = datetime.combine(selected_date, datetime.min.time().replace(hour=end_hour))

        Reservation.objects.create(
            user=request.user,
            room=room,
            student_id=request.user.username,
            start_time=start_datetime,
            end_time=end_datetime
        )

        return render(request, "testApp/reservation_success.html", {
            "room": room,
            "start": start_hour,
            "end": end_hour,
            "date": selected_date,
        })

    return render(request, "testApp/time_select.html", {
        "room": room,
        "time_slots": time_slots,
        "booked_hours": booked_hours,
        "selected_date": selected_date,
    })

# -------------------
# MY RESERVATIONS
# -------------------
@login_required(login_url="login")
def my_reservations_view(request):
    reservations = Reservation.objects.filter(
        user=request.user
    ).select_related("room", "room__building").order_by("-start_time")
    return render(request, "testApp/my_reservations.html", {
        "reservations": reservations
    })


# -------------------
# CANCEL RESERVATION
# -------------------
@login_required(login_url="login")
def cancel_reservation_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == "POST":
        reservation.delete()
    return redirect("my_reservations")