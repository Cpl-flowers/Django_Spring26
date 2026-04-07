from django.db import models

# Create your models here.
# when making a new migration use the command line
# python manage/py makemigrations testApp
# testApp being the name of the folder where the migrations are held
class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.IntegerField(null=True)
  joined_date = models.DateField(null=True)
  Email = models.CharField(null=True)