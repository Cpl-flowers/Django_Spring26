from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Building, Member
from django.template import loader

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

def about(request):
    template = loader.get_template('testApp/about.html')
    return HttpResponse(template.render())

def members(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('testApp/contact.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    mymember = Member.objects.get(id=id)
    template = loader.get_template('testApp/details.html')
    context = {
        'mymember': mymember,
    }
    return HttpResponse(template.render(context, request))