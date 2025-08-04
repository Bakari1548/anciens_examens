from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import View
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm


class LoginPageView(View):
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(
            request, 
            self.template_name, 
            context={ 'form': form, 'message': message }
        )
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                # email = form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password = form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                print("User connected. ", user)
                return redirect(settings.LOGIN_REDIRECT_URL)
        message = 'Les identifiants entrés sont incorrects.'
        return render(
            request,
            self.template_name,
            context={ 'form': form, 'message': message,}
        )
    

class SignUpView(View):
    template_name = 'authentication/register.html'
    form_class = forms.SignupForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(
            request, 
            self.template_name,
            context={ 'form': form, 'message': message}
        )
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        message = 'Veuillez verifier les informations saisies.'
        return render(
            request,
            self.template_name,
            context={ 'form': form, 'message': message }
        )
    

def logout_user(request):
    logout(request)
    print("User logged out successfully.")
    return redirect(settings.LOGOUT_REDIRECT_URL)  


def password_change(request):
    if request.method == 'POST':
        # recuperer les donnees mis a jour
        form = forms.PasswordChangeForm(user=request.user, data=request.POST or None)
        # si c'est valide, on enregistre
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/')
    else:
        # Sinon pas de changement
        form = forms.PasswordChangeForm(user=request.user)
    return render(
        request, 
        'authentication/password_change.html', 
        {'form': form}
    )

