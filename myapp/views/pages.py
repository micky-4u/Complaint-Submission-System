from django.shortcuts import render, redirect
from myapp.forms import LoginForm, SignupForm
from django.core.mail import EmailMessage
from django.contrib import messages
from myapp.models import  Issues
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.urls import reverse
from django.template.defaulttags import csrf_token
import uuid
from myapp.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


@login_required(login_url='myapp:login')
def home(request):
    if request.method == "POST":
        category = request.POST.get('category')
        room_number = request.POST.get('room_number')
        description = request.POST.get('description')
        
        issue = Issues(category =category, room_number=room_number, description =description)
        issue.save()
        
        send_complaint("anokyefadom@gmail.com", "COMPLAINT ALERT",f"Category: {category} \nRoom Number: {room_number} \nIssue ID: {issue.issue_id}\n\n\n\nComplaint: \n{description} ")
        
    return render(request, "home.html")


def complaintHistory(request):
    issues = Issues.objects.all().values
    context = {"issues": issues}
    return render(request, "complaintHistory.html",context)


def help(request):
    return render(request, "help.html")


def changePin(request):
    if request.method == 'POST':
        old = request.POST.get('password1')
        new1 = request.POST.get('password2')
        new2 = request.POST.get('password3')
        
        user = User.objects.get(username__exact = old )
        print(new1)
        if new1 == new2:
            user.set_password(new1)
            user.save()
            login(request, user)
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('myapp:success')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        messages.add_message(request, messages.ERROR,
                                 'Error validating, try again')
    return render(request, "changePin.html")



def success(request):
    return render(request, "success.html")


def custom_404(request):
    return render(request, '404.html', status=404)



def send_complaint(recipient, subject, body):
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