from django.shortcuts import render, redirect
from myapp.forms import LoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.contrib import messages
from myapp.models import User
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.urls import reverse


def landingPage(request):
    return render(request, "landingPage.html")


def signUp(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            hall = form.cleaned_data['hall']
            password2 = password1

            try:
                user = User.objects.get(email=email)
                messages.error(request, "Email already exists.")
                return redirect('login')
            except User.DoesNotExist:
                if password1 == password2:
                    user = User.objects.create(
                        email=email, username=email, first_name=hall)
                    user.set_password(password1)
                    user.save()
                    send_activation_email(user, request)
                    messages.add_message(request, messages.SUCCESS,
                                         'We sent you an email to verify your account')
                    return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            return redirect('signup')
    else:
        form = SignupForm()

        context = {'form': form}

    return render(request, "signUp.html", context)


def verifyAccount(request):
    return render(request, "verifyAccountPage.html")


def login(request):
    form = LoginForm(request.POST or None)
    context = {'form': form, 'page': 'login'}

    # if user is authenticated, redirect to home, when user tries to access login
    # if request.user.is_authenticated:
    #     return redirect('home')

    # Check if user is authenticated before login to home
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user and not user.is_email_verified:
                messages.add_message(request, messages.ERROR,
                                     'Email is not verified, please check your email inbox')
                return render(request, 'authenticate/login.html', context, status=401)
            elif user is not None and user.is_email_verified:
                login(request, user)
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR,
                                     'Invalid credentials, try again')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error validating, try again')

    return render(request, "login.html", context)


# Authentications
def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'

    # render a template file and pass in context
    email_body = render_to_string('authenticate/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
    })

    # create an email from using EmailMessage()
    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )
    # send email
    email.send()
