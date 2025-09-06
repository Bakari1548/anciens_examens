from django.contrib import admin
from django.urls import path, include
from django.conf import settings
import examens.views
import authentication.views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # App authentication
    path('admin/', admin.site.urls),
    path('', examens.views.home, name='home'),  # path vers la page d'accueil

    # Urls authentication
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
    path('password-change/', authentication.views.password_change, name='password-change'), # vue base sur une fonction

    path(
        'password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='authentication/password_reset.html',
            email_template_name='authentication/password_reset_email.html',
            subject_template_name='authentication/password_reset_subject.txt'    
        ), 
        name="password_reset"
    ),
    path(
        'password-reset/done', 
        auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), 
        name="password_reset_done"
    ),
    path(
        'reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), 
        name="password_reset_confirm"
    ),
    path(
        'reset/complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), 
        name="password_reset_complete"
    ),


    # App examens
    path('examens/<int:examen_id>/', examens.views.read_exam, name='read_exam'),
    path('examens/ajouter-examen', examens.views.post_exam, name='post_exam')
]

if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
