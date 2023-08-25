from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import logins, pages
# from django.http import Http404


app_name = "myapp"

urlpatterns = [
    path('', logins.landingPage, name="landingPage"),
    path('signup', logins.signUp, name="signup"),
    path('login', logins.login, name="login"),
    path('logout', logins.logout_view, name="logout"),
    path('verifyaccount', logins.verifyAccount, name="verifyaccount"),
    path('home', pages.home, name="home"),
    path('history', pages.complaintHistory, name="history"),
    path('help', pages.help, name="help"),
    path('changePin', pages.changePin, name="changePin"),
    path('success', pages.success, name="success"),
    
        re_path(r'^.*/$', pages.custom_404),

]
