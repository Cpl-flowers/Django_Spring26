from django.contrib import admin
from django.urls import path
from testApp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Room booking flow
    path('building/<int:building_id>/rooms/', views.select_room_view, name='select_rooms'),
    path('room/<int:room_id>/time/', views.time_select_view, name='time_select'),

    # Reservations
    path('my-reservations/', views.my_reservations_view, name='my_reservations'),
    path('cancel/<int:reservation_id>/', views.cancel_reservation_view, name='cancel_reservation'),
]