from django.core.mail import send_mail
from django.conf import settings
from .models import EmailVerification

def send_code_by_email(user, verification):
    # les parametres d'email pour envoyer le code 
    subject = 'Confirmation de votre email'
    message = f'''
    Bonjour {user.username},
    
    Votre code de vérification est : {verification.code}
    
    Ce code expirera dans 15 minutes.
    
    Cordialement,
    Anciens Examens Team
    '''
    from_email = settings.DEFAULT_FROM_EMAIL
    # envoie du code avec les parametres d'envoie d'email
    send_mail(subject, message, from_email, [user.email])

def send_verification_code(user):
    # Supprimer les anciennes vérifications
    EmailVerification.objects.filter(user=user).delete()

    # Créer une nouvelle verification
    verification = EmailVerification.objects.create(
        user=user, 
        code=EmailVerification.generate_code()
    )

    # Envoyer l'email
    send_code_by_email(user, verification)

    return verification