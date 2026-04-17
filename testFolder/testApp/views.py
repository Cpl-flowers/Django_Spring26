from django.shortcuts import render, get_object_or_404
from .models import Building
from .models import Building, Room

def home(request):
    buildings = Building.objects.all()
    return render(request, 'testApp/home.html', {'buildings': buildings})


def login_view(request):
    return render(request, 'testApp/login.html')


def signup_view(request):
    return render(request, 'testApp/login.html')


# STEP 1: select rooms in building
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

# STEP 2: time selection page
def time_select_view(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    time_slots = list(range(8, 18))  # 8AM → 5PM

    return render(request, 'testApp/time_select.html', {
        'room': room,
        'time_slots' : time_slots
    })

def reservation_page(request, room_id):

    room = get_object_or_404(Room, id=room_id)

    return render(
        request,
        'testApp/reservation.html',
        {
            'room': room
        }
    )