from django.shortcuts import render, redirect
from myapp.forms import LoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.contrib import messages
from myapp.models import User, Issues
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.urls import reverse
from django.template.defaulttags import csrf_token
import uuid


def home(request):
    if request.method == "POST":
        form = Issues(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            room_number = form.cleaned_data['room_number']
            description = form.cleaned_data['description']

            issue = Issues.objects.create(
                category=category, room_number=room_number, description=description)

            issue.save()

    return render(request, "home.html")


def complaintHistory(request):
    return render(request, "complaintHistory.html")


def help(request):
    return render(request, "help.html")


def changePin(request):
    return render(request, "changePin.html")


def success(request):
    return render(request, "success.html")
