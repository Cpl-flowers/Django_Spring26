from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Building, Member


def home(request):
    buildings = Building.objects.all()
    return render(request, 'testApp/home.html', {'buildings': buildings})


def login_view(request):
    return render(request, 'testApp/login.html')


def signup_view(request):
    return render(request, 'testApp/login.html')


def homePage(request):
    template = loader.get_template('homePage.html')
    return HttpResponse(template.render())


def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())


def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())


def members(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('contact.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))


def details(request, id):
    mymember = Member.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'mymember': mymember,
    }
    return HttpResponse(template.render(context, request))