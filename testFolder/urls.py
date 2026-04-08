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

    # use to turn on the virtual enviroment source virt/Scripts/activate
    
"""
from django.contrib import admin
from django.urls import include, path
from studyroom import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('homePage/', views.homePage, name='Home'),
    path('homePage/contact/', views.members, name='HomeContact'),
    path('about/', views.about, name='About'),
    path('contact/', views.members, name='Contact'),
    path('contact/details/<int:id>', views.details, name='Details'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]