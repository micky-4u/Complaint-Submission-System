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
                'placeholder': 'eg. eu@st.ug.edu'

            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": " inputText",
                "placeholder": "Enter your student number",
                'id': "floatingInput1",
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "toggleable-password inputText",
                "placeholder": "eg. 10645372",
                'id': "floatingInput1",
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "toggleable-password inputText",
                "placeholder": "Re-enter your student pin",
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

    first_name = forms.ChoiceField(
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
        fields = ['email', 'username', 'password1', 'password2', 'first_name']

        def save(self, commit=True):
            user = super(SignupForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            user.password1 = self.cleaned_data['password1']
            user.hall = self.cleaned_data['first_name']
            user.password2 = self.cleaned_data['password2']
            user.username = self.cleaned_data['username']

            if commit:
                user.save()

            return user

# create a login form


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": " inputText",
                "placeholder": "Enter your student number",
                'id': "floatingInput1",
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


# class Issue(forms.Form):
#     CHOICES = (
#         ('CA', 'Capentrey'),
#         ('WA', 'Water'),
#         ('LI', 'Light'),
#     )
#     category = forms.ChoiceField(
#     label="category",
#     choices=CHOICES,
#     widget=forms.Select(
#         attrs={
#             # "class": "inputText",
#             "placeholder": "Eg. Capentery",
#             "id": "category",
#         }
#     )
#     )

#     room_number = forms.CharField(
#         label="Pin",
#         widget=forms.TextInput(
#             attrs={
#                 "class": "inputText",
#                 "autocomplete": "password",
#                 "placeholder": "Eg",
#                 "id": "floatingPassword",
#             }
#         )

#     )
#     class Meta:
#         model = Issues
#         fields = ['category']
