from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Building

def home(request):
    buildings = Building.objects.all()
    return render(request, 'testApp/home.html', {'buildings': buildings})

def login_view(request):
    return render(request, 'testApp/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'testApp/signup.html', {'form': form})