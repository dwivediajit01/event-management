# authapp/forms.py

from django import forms
from django.contrib.auth.models import User


ROLE_CHOICES = [
        ('EventManager', 'Event Manager'),
        ('Attendee', 'Attendee'),
    ]

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Login As")