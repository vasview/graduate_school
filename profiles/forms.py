from django import forms
from django.forms.widgets import DateInput

from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'middle_name', 'mobile', 'personal_number', 'birth_date', 'gender')