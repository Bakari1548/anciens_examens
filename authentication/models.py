from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from .validators import validate_univ_thies_email
import random
import string



class User(AbstractUser):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(validators=[validate_univ_thies_email], unique=True)
    
    def __str__(self):
        return self.username

    
class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    # convertir les fonctions en method utilisables
    @classmethod
    def generate_code(cls):
        # Generer un code à 6 caracteres
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def is_expired(self):
        # Verifier si le code a expire (15 minutes de validite)
        from django.utils import timezone
        # comparer l'heure actuel et l'heure ou le code est genere (created_at)
        return (timezone.now() - self.created_at).total_seconds() > 900  # 15 * 60sec