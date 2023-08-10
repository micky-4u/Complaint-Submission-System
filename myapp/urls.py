from django.urls import path, re_path
# from django.contrib.auth import views as auth_views
from .views import logins
# from django.http import Http404


urlpatterns = [
    path('', logins.landingPage, name="landingPage"),
    path('signup', logins.signUp, name="signUp"),
    path('login', logins.login, name="login"),
    path('verifyaccount', logins.verifyAccount, name="verifyaccount"),
]
