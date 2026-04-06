from django.shortcuts import render
from .models import Building


def home(request):
    buildings = Building.objects.all()
    return render(request, 'testApp/home.html', {'buildings': buildings})


def login_view(request):
    return render(request, 'testApp/login.html')


def signup_view(request):
    return render(request, 'testApp/login.html')