"""
URL configuration for testFolder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from testApp import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),

    # STEP 1 → rooms in building
    path('building/<int:building_id>/rooms/', views.select_room_view, name='select_rooms'),

    # STEP 2 → time selection
    path('room/<int:room_id>/time/', views.time_select_view, name='time_select'),

    path('reserve/<int:room_id>/', views.my_reservations_view, name='reservation_page'),

    path('my-reservations/', views.my_reservations_view, name='my_reservations'),

    path('my-reservations/', views.my_reservations_view, name='my_reservations'),

    
]