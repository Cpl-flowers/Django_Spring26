from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from django.views.decorators.http import require_POST
from datetime import datetime
from .models import Building, Room, Reservation, Member, CheckIn

def room_is_booked_today(room, date):
    if not room.available:
        return True

    time_slots = list(range(8, 18))
    reservations = Reservation.objects.filter(room=room, start_time__date=date)
    booked_hours = set()
    for r in reservations:
        start = r.start_time.hour
        end = r.end_time.hour
        booked_hours.update(range(start, end))
    return len(booked_hours) >= len(time_slots)



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

    # Add room counts to each building based on today's bookings
    today = datetime.now().date()
    for building in buildings:
        rooms = building.room_set.all()
        total_rooms = rooms.count()
        available_rooms = 0
        for room in rooms:
            if not room_is_booked_today(room, today):
                available_rooms += 1
        unavailable_rooms = total_rooms - available_rooms
        building.total_rooms = total_rooms
        building.available_rooms = available_rooms
        building.unavailable_rooms = unavailable_rooms
        building.availability_percent = int((available_rooms / total_rooms * 100) if total_rooms > 0 else 0)

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
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")

        if not username or not password or not password_confirm:
            error = "All fields are required."
        elif password != password_confirm:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "This username is already taken. Please choose another."
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect("home")

    return render(request, 'testApp/signup.html', {"error": error})

@login_required(login_url="login")
@require_POST
def check_in_view(request):
    CheckIn.objects.create(user=request.user)

    messages.success(request, "You checked in successfully.")
    return redirect("home")


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
# API - BUILDING ROOM COUNTS
# -------------------
def api_building_counts(request):
    """Return room availability counts for all buildings as JSON."""
    buildings = Building.objects.all()
    data = {}
    today = datetime.now().date()
    
    for building in buildings:
        rooms = building.room_set.all()
        total_rooms = rooms.count()
        available_rooms = sum(1 for room in rooms if not room_is_booked_today(room, today))
        unavailable_rooms = total_rooms - available_rooms
        availability_percent = int((available_rooms / total_rooms * 100) if total_rooms > 0 else 0)
        
        data[building.id] = {
            'total_rooms': total_rooms,
            'available_rooms': available_rooms,
            'unavailable_rooms': unavailable_rooms,
            'availability_percent': availability_percent
        }
    
    return JsonResponse(data)

# -------------------
# STEP 1 - SELECT ROOM
# -------------------
def select_room_view(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    rooms = Room.objects.filter(building=building)
    selected_date = datetime.now().date()
    for room in rooms:
        room.booked_today = room_is_booked_today(room, selected_date)

    seat_filter = request.GET.get('seats')
    if seat_filter:
        rooms = rooms.filter(seating__gte=seat_filter)

    return render(request, 'testApp/select_room.html', {
        'building': building,
        'rooms': rooms,
        'selected_date': selected_date,
        'error': request.GET.get('error')
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
    fully_booked = room_is_booked_today(room, selected_date)

    if fully_booked:
        building = room.building
        rooms = Room.objects.filter(building=building)
        selected_date = selected_date
        for r in rooms:
            r.booked_today = room_is_booked_today(r, selected_date)
        return render(request, 'testApp/select_room.html', {
            'building': building,
            'rooms': rooms,
            'selected_date': selected_date,
            'error': f'Room {room.number} is fully booked for {selected_date}. Please choose another room.'
        })

    if request.method == "POST":
        start_hour = int(request.POST.get("start_time"))
        end_hour = int(request.POST.get("end_time"))

        # Validate that end time is after or equal to start time (inclusive booking)
        if end_hour < start_hour:
            return render(request, "testApp/time_select.html", {
                "room": room,
                "time_slots": time_slots,
                "booked_hours": booked_hours,
                "selected_date": selected_date,
                "error": "End time must be the same or later than start time."
            })

        # Check for booking conflicts using inclusive end time
        for h in range(start_hour, end_hour + 1):
            if h in booked_hours:
                return render(request, "testApp/time_select.html", {
                    "room": room,
                    "time_slots": time_slots,
                    "booked_hours": booked_hours,
                    "selected_date": selected_date,
                    "error": "That time is already booked!"
                })

        start_datetime = datetime.combine(selected_date, datetime.min.time().replace(hour=start_hour))
        end_datetime = datetime.combine(selected_date, datetime.min.time().replace(hour=end_hour + 1))

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
            "duration": end_hour - start_hour + 1,
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
