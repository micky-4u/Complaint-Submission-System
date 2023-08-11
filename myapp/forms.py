from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Issues


# inherit UserCreationForm to create SignupForm
class SignupForm(UserCreationForm):
    email = forms.EmailField(
        label="ID Number/Email",
        widget=forms.EmailInput(
            attrs={
                "class": "inputText",
                "autocomplete": "email",
                'id': "floatingInput",
                'placeholder': 'eg. 10645372'

            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "toggleable-password inputText",
                "placeholder": "Enter your student pin",
                'id': "floatingInput1",
            }
        )
    )

    CHOICES = (
        ('PENT', 'African Union Hall'),
        ('LH', 'Legon Hal'),
        ('AK', 'Akuafo Hall-'),
        ('VANDAL', 'Commonwealth Hall-'),
        ('UGEL', 'UGEL Halls'),
    )

    hall = forms.ChoiceField(
        label="Hall",
        choices=CHOICES,
        widget=forms.Select(
            attrs={
                # "class": "inputText",
                "placeholder": "Eg. Legon Hall",
                "id": "floatingPassword",
            }
        )
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'first_name']


# create a login form
class LoginForm(forms.Form):
    email = forms.EmailField(
        label="ID Number/Email",
        widget=forms.EmailInput(
            attrs={
                "class": "inputText",
                "autocomplete": "email",
                'id': "floatingInput",
                'placeholder': 'eg. 18654783'
            }
        )
    )

    password = forms.CharField(
        label="Pin",
        widget=forms.PasswordInput(
            attrs={
                "class": "toggleable-password inputText",
                "autocomplete": "password",
                "placeholder": "Enter your student pin",
                "id": "floatingPassword",
            }
        )
    )


class Issue(forms.Form):
    CHOICES = (
        ('PENT', 'African Union Hall'),
        ('LH', 'Legon Hal'),
        ('AK', 'Akuafo Hall-'),
        ('VANDAL', 'Commonwealth Hall-'),
        ('UGEL', 'UGEL Halls'),
    )
    category = forms.ChoiceField(
    label="category",
    choices=CHOICES,
    widget=forms.Select(
        attrs={
            # "class": "inputText",
            "placeholder": "Eg. Capentery",
            "id": "category",
        }
    )
    )
    
    class Meta:
        model = Issues
        fields = ['category']
