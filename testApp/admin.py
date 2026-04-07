from django.contrib import admin
from .models import Member

# Register your models here.
from .models import Building  # make sure this is imported

admin.site.register(Building)  # register it so you can see it in admin