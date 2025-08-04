"""
URL configuration for anciens_examens project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
import examens.views
import authentication.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', examens.views.home, name='home'),  # path vers la page d'accueil
    path(
        'connexion/', 
        authentication.views.LoginPageView.as_view(template_name='authentication/login.html'), 
        name='login'
    ), # view base sur une class 
    path(
        'inscription/', 
        authentication.views.SignUpView.as_view(template_name='authentication/register.html'), 
        name='register'
    ),  # view base sur une class 
    path('logout/', authentication.views.logout_user, name='logout'),
    path('password-change', authentication.views.password_change, name='password-change'),
]

if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
