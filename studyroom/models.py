from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    floor_count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.campus})"