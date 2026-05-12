from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("check-in/", views.check_in_view, name="check_in"),
    path("building/<int:building_id>/rooms/", views.select_room_view, name="select_rooms"),
    path("room/<int:room_id>/time/", views.time_select_view, name="time_select"),
    path("my-reservations/", views.my_reservations_view, name="my_reservations"),
    path("cancel/<int:reservation_id>/", views.cancel_reservation_view, name="cancel_reservation"),
]
