# use to turn on the virtual enviroment source virt/Scripts/activate

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member

# Create your views here.
# defines methods for each url pattern
def homePage(request):
  template = loader.get_template('homepage.html')
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

# takes the input of request and id
# the id is used to locate the correct record in the table
# then loads the detail template and sends the into the template
def details(request, id):
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
  }
  return HttpResponse(template.render(context, request))