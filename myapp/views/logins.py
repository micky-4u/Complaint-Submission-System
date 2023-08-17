from django.shortcuts import render, redirect
from myapp.forms import LoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage, send_mail
from django.contrib import messages
from myapp.models import User
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.urls import reverse
# from myapp.tokens import account_activation_token
import random


def landingPage(request):
    return render(request, "landingPage.html")


def signUp(request):
    print("Hello")
    if request.method == 'POST':
        form = SignupForm(request.POST)
        print(form)
        if form.is_valid():
            email_to = form.cleaned_data['email']

            global otp
            otp = random.randint(100000, 999999)
            print(otp)

            # user = form.save()

            messages.success(request, "Otp Sent")
            subject = "ACCOUNT VERIFICATION"
            email_from = settings.EMAIL_HOST_USER
            to_list = [email_to]
            message = f"Your verification code: /n {otp}"

            send_mail(subject, message, email_from,
                      to_list, fail_silently=True)
            print(email_to)
            print("Created")
            return redirect('myapp:confirmation')

        else:

            messages.error(request, "error")
            return redirect('myapp:signup')
    else:
        form = SignupForm()

    context = {'form': form}

    return render(request, "signUp.html", context)


def verifyAccount(request):
    if request.method == "POST":
        input1 = request.POST.get("input1")
        input2 = request.POST.get("input2")
        input3 = request.POST.get("input3")
        input4 = request.POST.get("input4")
        input5 = request.POST.get("input5")
        input6 = request.POST.get("input6")

        code = str(input1) + str(input2) + str(input3) + \
            str(input4) + str(input5) + str(input6)
        print(code)

        if code == str(otp):
            return redirect('myapp:home')
        else:
            print("nothin")

    return render(request, "verifyAccountPage.html")


def login(request):
    form = LoginForm(request.POST or None)
    context = {'form': form, 'page': 'login'}

    # if user is authenticated, redirect to home, when user tries to access login
    if request.user.is_authenticated:
        return redirect('myapp:home')

    # Check if user is authenticated before login to home
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user and not user.is_email_verified:
                messages.add_message(request, messages.ERROR,
                                     'Email is not verified, please check your email inbox')
                return render(request, 'login.html', context, status=401)
            elif user is not None and user.is_email_verified:
                login(request, user)
                return redirect('myapp:home')
            else:
                messages.add_message(request, messages.ERROR,
                                     'Invalid credentials, try again')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error validating, try again')

    return render(request, "login.html", context)


# Authentications
def send_activation_email(user, request, code):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'

    # render a template file and pass in context
    email_body = render_to_string('verifyAccountPage.html', {
        'user': user,
        'domain': current_site,
        'confirmation code': code
    })

    # create an email from using EmailMessage()
    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )
    # send email
    email.send()
