from django.shortcuts import render, redirect
from myapp.forms import LoginForm, SignupForm
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.contrib import messages
from myapp.models import User
from django.contrib.auth import authenticate, login as log, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
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
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']


            global otp
            otp = random.randint(100000, 999999)
            print(otp)

            # user = form.save()
            print("/n/n about to send otp")
            try:
                user = User.objects.get(email=email_to)
                messages.error(request, "Email already exists.")
                return redirect('myapp:login')
            
                # send_otp(email_to,"ACCOUNT CONFIRMATION",f"Your confirmation code : {otp}")
                # print("Hello")
                # send_activation_email(email_to, request, otp)
            except User.DoesNotExist:
                if password1 == password2:
                    user = User.objects.create(email=email_to, username=username)
                    user.set_password(password1)
                    user.save()
                    log(request, user)
                    # send_activation_email(user, request)
                    send_otp(email_to,"ACCOUNT CONFIRMATION",f"Your confirmation code : {otp}")

                    messages.add_message(request, messages.SUCCESS,
                                         'We sent you confirmation code to verify your account')
                    return redirect('myapp:verifyaccount')
            
            # return redirect(reverse('myapp:verifyaccount'))

        else:

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
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
    # if request.user.is_authenticated:
    #     return redirect('myapp:home')

    # Check if user is authenticated before login to home
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if not user:
                messages.add_message(request, messages.ERROR,
                                     'User does not exit')
                return render(request, 'login.html', context, status=401)
            elif user :
                log(request, user)
                return redirect('myapp:home')
            else:
                messages.add_message(request, messages.ERROR,
                                     'Invalid credentials, try again')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error validating, try again')

    return render(request, "login.html", context)


# Authentications
# def send_activation_email(email, request, code):
#     email_subject = 'Activate your account'
#     current_site = get_current_site(request)
#     # render a template file and pass in context
#     email_body = render_to_string('verifyAccountPage.html', context={
#         'user': email,
#         'domain': current_site,
#         'confirmation code': code
#     })

#     # create an email from using EmailMessage()
#     email = EmailMessage(subject=email_subject, body=email_body,
#                          from_email=settings.EMAIL_HOST_USER,
#                          to=[email]
#                          )
#     # send email
#     email.send()
    
    
def send_otp(recipient, subject, body):
    import smtplib

    FROM = "complaint System Application"
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(FROM, TO, message)
        server.close()
        print ('successfully sent the mail')
    except:
        print ("failed to send mail")

from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('myapp:login')



