from django.db import models
from django.contrib.auth.models import User


class Building(models.Model):
    name = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    floor_count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.campus})"


class Room(models.Model):
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    floor = models.CharField(max_length=50)
    seating = models.IntegerField()

    has_outlets = models.BooleanField(default=True)
    has_wifi = models.BooleanField(default=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - Room {self.number}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    student_id = models.CharField(max_length=20)

    # Time-based reservation (supports real scheduling + overlap checking)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.room.number}"