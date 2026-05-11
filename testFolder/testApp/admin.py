from django.contrib import admin
from .models import Building, Room, Reservation, Member, CheckIn

admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Member)
admin.site.register(CheckIn)
