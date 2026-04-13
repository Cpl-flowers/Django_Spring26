from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from studyroom import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='Login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='Logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='Home'),
    path('about/', views.about, name='About'),
    path('contact/', views.members, name='Contact'),
    path('signup/', views.signup_view, name='signup'),
    path('details/<int:id>/', views.details, name='Details'),
]