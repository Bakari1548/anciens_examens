from django.shortcuts import render, redirect
from . import forms, models
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import View
from .services import send_verification_code


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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # email=form.cleaned_data['email'],
            try:
                data_user = models.User.objects.get(username=username)
            except models.User.DoesNotExist:
                messages.error(request, 'Cet utilisateur n\'existe pas.')

            user = authenticate(request, username=username, password=password)
            # Vérifier si les donnees de l'utilisateur sont remplies
            # Et si le compte est activé (email universitaire verifié)
            if user is not None and data_user.is_active:
                login(request, user)
                messages.success(request, 'Utilisateur connecté avec succès !')
                print("User connected.", user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, 'Identifiants incorrects.')
        message = 'Identifiants incorrects. Veuillez vérifier votre nom d\'utilisateur et mot de passe.'
        return render(
            request,
            self.template_name,
            context={ 'form': form, 'message': message,}
        )
    
def register(request):
    template_name = 'authentication/register.html'
    form_class = forms.SignupForm

        
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            print(form)
            # Enregistrer les donnees sans les envoyer dans la base de donnees
            user = form.save(commit=False)
            user.is_active = False   # Desactiver le code jusqu'a verification
            user.save()

            #  Envoyer le code de verification par email
            send_verification_code(user)
            messages.success(request, 'Un code de vérification a été envoyé à votre email.')

            # rediriger vers le template de la verification de l'email universitaire
            return redirect('verify-email', user_id=user.id)
        # print(request.POST)
        return render(
            request,
            template_name,
            context={ 'form': form }
        )
    else:
        form = form_class()
    

    return render(
        request, 
        template_name,
        context={ 'form': form }
    )
    

def verify_email(request, user_id): # class pour envoyer un code a l'utilisateur
    verification = models.EmailVerification()
    template_name = 'authentication/verify_email.html'
    form_class = forms.VerifyEmailForm
    message_error = ''
    try:
        user = models.User.objects.get(id=user_id)
        verification = models.EmailVerification.objects.get(user=user)
    except (models.User.DoesNotExist, models.EmailVerification.DoesNotExist):
        messages.error(request, 'Utilisateur ou code de verification introuvable.')
        return redirect('register')

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid:
            code = form.data.get('code').lower()
            print(code)
            if verification.is_expired():
                messages.error(request, 'Le code a expiré. Un nouveau code a été envoyé.')
                send_verification_code(user)
                return redirect('verify_email', user_id=user.id)
            
            if verification.code.lower() == code:
                verification.is_expired = True
                verification.is_verified = True
                verification.save()

                # Activer l'utilisateur
                user.is_active = True
                user.save()

                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                message_error = "Le code que vous avez entré est incorrect."
                messages.error(request, 'Le code que vous avez entré est incorrect.')

            print("donnees de la requete POST: ", request.POST)
    
    else:
        form = form_class()
    
    return render(
        request,
        template_name,
        context={ 'form': form, 'message_error': message_error }
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
            messages.success(request, 'Mot de passe mis à jour avec succès !')
            return redirect('/')
        else:
            messages.error(request, 'Veuillez revoir les données entrées svp.')
    else:
        # Sinon pas de changement
        form = forms.PasswordChangeForm()
    return render(
        request, 
        'authentication/password_change.html', 
        {'form': form}
    )



def send_mail_page(request):
    context = {}

    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            try:
                send_mail(settings.EMAIL_HOST_USER, [email])
                context['result'] = 'Email sent successfully'
            except Exception as e:
                context['result'] = f'Error sending email: {e}'
        else:
            context['result'] = 'All fields are required'
    
    return render(
        request, 
        "authentication/password_reset.html", 
        context
    )
