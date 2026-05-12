from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Building, CheckIn, Reservation, Room


def room_is_booked_today(room, date):
    if not room.available:
        return True

    time_slots = list(range(8, 18))
    reservations = Reservation.objects.filter(room=room, start_time__date=date)
    booked_hours = set()

    for reservation in reservations:
        booked_hours.update(range(reservation.start_time.hour, reservation.end_time.hour))

    return len(booked_hours) >= len(time_slots)


def home(request):
    buildings = Building.objects.all()

    search = request.GET.get("search", "")
    if search:
        buildings = buildings.filter(name__icontains=search) | buildings.filter(campus__icontains=search)

    campus = request.GET.get("campus", "")
    if campus and campus != "All Campuses":
        buildings = buildings.filter(campus=campus)

    if request.GET.get("available", ""):
        buildings = buildings.filter(room__available=True).distinct()

    today = datetime.now().date()
    for building in buildings:
        rooms = building.room_set.all()
        total_rooms = rooms.count()
        available_rooms = sum(1 for room in rooms if not room_is_booked_today(room, today))

        building.total_rooms = total_rooms
        building.available_rooms = available_rooms
        building.unavailable_rooms = total_rooms - available_rooms
        building.availability_percent = int((available_rooms / total_rooms * 100) if total_rooms else 0)

    return render(request, "testApp/home.html", {
        "buildings": buildings,
        "search": search,
        "campus": campus,
    })


def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.POST.get("next") or request.GET.get("next") or "home")

        error = "Invalid credentials. Please use your UTRGV username and password."

    return render(request, "testApp/login.html", {
        "error": error,
        "next": request.GET.get("next", ""),
    })


def logout_view(request):
    logout(request)
    return redirect("home")


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "testApp/signup.html", {"form": form})


@login_required(login_url="login")
@require_POST
def check_in_view(request):
    CheckIn.objects.create(user=request.user)
    messages.success(request, "You checked in successfully.")
    return redirect("home")


def api_building_counts(request):
    buildings = Building.objects.all()
    today = datetime.now().date()
    data = {}

    for building in buildings:
        rooms = building.room_set.all()
        total_rooms = rooms.count()
        available_rooms = sum(1 for room in rooms if not room_is_booked_today(room, today))

        data[building.id] = {
            "total_rooms": total_rooms,
            "available_rooms": available_rooms,
            "unavailable_rooms": total_rooms - available_rooms,
            "availability_percent": int((available_rooms / total_rooms * 100) if total_rooms else 0),
        }

    return JsonResponse(data)


def select_room_view(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    rooms = Room.objects.filter(building=building)
    selected_date = datetime.now().date()

    seat_filter = request.GET.get("seats")
    if seat_filter:
        rooms = rooms.filter(seating__gte=seat_filter)

    for room in rooms:
        room.booked_today = room_is_booked_today(room, selected_date)

    return render(request, "testApp/select_room.html", {
        "building": building,
        "rooms": rooms,
        "selected_date": selected_date,
        "error": request.GET.get("error"),
    })


def time_select_view(request, room_id):
    if not request.user.is_authenticated:
        return redirect("login")

    room = get_object_or_404(Room, id=room_id)
    time_slots = list(range(8, 18))

    selected_date_str = request.GET.get("date", "") or request.POST.get("date", "")
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = datetime.now().date()
    else:
        selected_date = datetime.now().date()

    reservations = Reservation.objects.filter(room=room, start_time__date=selected_date)
    booked_hours = set()
    for reservation in reservations:
        booked_hours.update(range(reservation.start_time.hour, reservation.end_time.hour))

    if room_is_booked_today(room, selected_date):
        building = room.building
        rooms = Room.objects.filter(building=building)
        for building_room in rooms:
            building_room.booked_today = room_is_booked_today(building_room, selected_date)

        return render(request, "testApp/select_room.html", {
            "building": building,
            "rooms": rooms,
            "selected_date": selected_date,
            "error": f"Room {room.number} is fully booked for {selected_date}. Please choose another room.",
        })

    if request.method == "POST":
        start_hour = int(request.POST.get("start_time"))
        end_hour = int(request.POST.get("end_time"))

        if end_hour < start_hour:
            return render(request, "testApp/time_select.html", {
                "room": room,
                "time_slots": time_slots,
                "booked_hours": list(booked_hours),
                "selected_date": selected_date,
                "error": "End time must be the same or later than start time.",
            })

        for hour in range(start_hour, end_hour + 1):
            if hour in booked_hours:
                return render(request, "testApp/time_select.html", {
                    "room": room,
                    "time_slots": time_slots,
                    "booked_hours": list(booked_hours),
                    "selected_date": selected_date,
                    "error": "That time is already booked!",
                })

        start_datetime = datetime.combine(selected_date, datetime.min.time().replace(hour=start_hour))
        end_datetime = datetime.combine(selected_date, datetime.min.time().replace(hour=end_hour + 1))

        Reservation.objects.create(
            user=request.user,
            room=room,
            student_id=request.user.username,
            start_time=start_datetime,
            end_time=end_datetime,
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
        "booked_hours": list(booked_hours),
        "selected_date": selected_date,
    })


@login_required(login_url="login")
def my_reservations_view(request):
    reservations = Reservation.objects.filter(
        user=request.user,
    ).select_related("room", "room__building").order_by("-start_time")

    return render(request, "testApp/my_reservations.html", {"reservations": reservations})


@login_required(login_url="login")
def cancel_reservation_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if request.method == "POST":
        reservation.delete()

    return redirect("my_reservations")
