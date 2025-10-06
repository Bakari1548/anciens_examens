from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from .validators import validate_univ_thies_email


class LoginForm(forms.Form):
    # email = forms.EmailField(max_length=63, label="Email")
    username = forms.CharField(max_length=63, label="Nom d'utilisateur")
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Mot de passe")

class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=63, 
        label="Nom d'utilisateur",
        error_messages={
            'required': 'Ce nom d\'utilisateur a été dèjà utilisé, veuillez choisir un autre',
            'invalid': 'Ce nom d\'utilisateur a été dèjà utilisé, veuillez choisir un autre'
        },
    )
    first_name = forms.CharField(label="Prénom", max_length=200)
    last_name = forms.CharField(label="Nom", max_length=100)
    email = forms.EmailField(
        label='Email universitaire',
        validators=[
            validate_univ_thies_email
        ],
        help_text='Vous devez obligatoirement vous inscrire avec votre email universitaire (...@univ-thies.sn)',
        error_messages= {
            'required': 'Veuiller saisir votre email unoversitaire',
            'invalid': 'Vous devez utiliser votre email universitaire pour vous inscrire !',
            'unique': 'Un utilisateur avec cet email existe déjà.',
        },
    )
    password1 = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Mot de passe")
    password2 = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Confirmer mot de passe")
    class Meta():
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        
class VerifyEmailForm(forms.Form):
    code = forms.CharField(
        max_length=6, 
        min_length=6,
        label="Entrez le code à 6 caractères"
    )
    
    
class PasswordChangeForm(forms.Form):
    oldpassword = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Ancien mot de passe")
    password1 = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Nouveau mot de passe")
    password2 = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Confirmer mot de passe")