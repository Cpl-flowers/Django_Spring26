# use to turn on the virtual enviroment source virt/Scripts/activate

from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # url patterns to define web pages
    # redirect the root URL to the home page for user convenience
    path('', RedirectView.as_view(url='/homePage/', permanent=False), name='RootRedirect'),
    path('homePage/', views.homePage, name='Home'),
    path('homePage/contact/', views.members, name='HomeContact'),
    path('about/', views.about, name='About'),
    path('contact/', views.members, name='Contact'),
    path('contact/details/<int:id>', views.details, name='Details'),
    path('login/', views.login, name='Login')
]