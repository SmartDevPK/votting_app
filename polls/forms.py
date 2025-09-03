from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Poll, Choice  # Make sure the model names match your models.py

# User Registration Form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# Poll Form
class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ["question"]

# Choice Form
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["choice_text"]
