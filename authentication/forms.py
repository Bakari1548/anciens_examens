from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model



class LoginForm(forms.Form):
    # email = forms.EmailField(max_length=63, label="Email")
    username = forms.CharField(max_length=63, label="Nom d'utilisateur")
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Mot de passe")

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=63, label="Email universitaire")
    username = forms.CharField(max_length=63, label="Nom d'utilisateur")
    password1 = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Mot de passe")
    password2 = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Confirmer mot de passe")
    class Meta():
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')
    
class PasswordChangeForm(PasswordChangeForm):
    oldpassword = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Ancien mot de passe")
    password1 = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Nouveau mot de passe")
    password2 = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Confirmer mot de passe")

    class Meta():
        # fields = ('old_password', 'new_password1', 'new_password2')
        fields = 'oldpassword, password1, password2'

