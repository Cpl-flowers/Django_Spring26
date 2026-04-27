from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from datetime import datetime

from .models import Building, CheckIn, Room, Reservation


# -------------------
# HOME PAGE
# -------------------
def home(request):
    buildings = Building.objects.all()

    return render(request, 'testApp/home.html', {
        'buildings': buildings
    })


# -------------------
# LOGIN / SIGNUP
# -------------------
def login_view(request):
    return render(request, 'testApp/login.html')


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, 'testApp/signup.html', {
        'form': form
    })


@login_required(login_url="login")
@require_POST
def check_in_view(request):
    CheckIn.objects.create(user=request.user)

    messages.success(request, "You checked in successfully.")
    return redirect("home")


# -------------------
# STEP 1 - ROOMS
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
# STEP 2 - TIME + RESERVATION SYSTEM
# -------------------
def time_select_view(request, room_id):

    room = get_object_or_404(Room, id=room_id)

    time_slots = list(range(8, 18))  # 8AM - 5PM

    # Get existing reservations for this room
    reservations = Reservation.objects.filter(room=room)

    booked_hours = []

    for r in reservations:
        start = r.start_time.hour
        end = r.end_time.hour

        for h in range(start, end):
            booked_hours.append(h)

    booked_hours = list(set(booked_hours))

    # -------------------
    # POST = user submits reservation
    # -------------------
    if request.method == "POST":

        start_hour = int(request.POST.get("start_time"))
        end_hour = int(request.POST.get("end_time"))

        # block overlap
        for h in range(start_hour, end_hour):
            if h in booked_hours:
                return render(request, "testApp/time_select.html", {
                    "room": room,
                    "time_slots": time_slots,
                    "booked_hours": booked_hours,
                    "error": "That time is already booked!"
                })

        # user must be logged in
        user = request.user

        if not user.is_authenticated:
            return redirect("login")

        today = datetime.now().date()

        start_datetime = datetime.combine(today, datetime.min.time().replace(hour=start_hour))
        end_datetime = datetime.combine(today, datetime.min.time().replace(hour=end_hour))

        Reservation.objects.create(
            user=user,
            room=room,
            student_id="TEMP",
            start_time=start_datetime,
            end_time=end_datetime
        )

        return render(request, "testApp/reservation_success.html", {
            "room": room,
            "start": start_hour,
            "end": end_hour
        })

    return render(request, "testApp/time_select.html", {
        "room": room,
        "time_slots": time_slots,
        "booked_hours": booked_hours
    })


# -------------------
# MY RESERVATIONS PAGE
# -------------------
def my_reservations_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    reservations = Reservation.objects.filter(
        user=request.user
     ).select_related("room", "room__building").order_by("-start_time")

    return render(request, "testApp/my_reservations.html", {
        "reservations": reservations
    })
