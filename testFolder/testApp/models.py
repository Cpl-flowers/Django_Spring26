from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    floor_count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.campus})"

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)
    Email = models.CharField(null=True)