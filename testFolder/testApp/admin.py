from django.contrib import admin
from .models import Member, Building  # make sure these are imported

# Register your models here.
admin.site.register(Member)  # register it so you can see it in admin
admin.site.register(Building)  # register it so you can see it in admin