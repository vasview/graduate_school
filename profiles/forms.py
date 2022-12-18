from django import forms
from django.forms.widgets import DateInput
from django.contrib.auth.forms import SetPasswordForm

from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'middle_name', 'mobile', 'personal_number', 'birth_date', 'gender')


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ('current_password', 'new_password1', 'new_password2')

    current_password = forms.CharField(max_length=50, label='Текущий пароль',
                        widget=forms.PasswordInput(attrs={'class':'form-control', 'id':"password", 'placeholder':'Текущий пароль'}))

    new_password1 = forms.CharField(max_length=50, label='Новый пароль',
                        widget=forms.PasswordInput(attrs={'class':'form-control', 'id':"password", 'placeholder':'Новый пароль'}))
    
    new_password2 = forms.CharField(max_length=50, label='Подтверждение нового пароля',
                        widget=forms.PasswordInput(attrs={'class':'form-control', 'id':"password", 'placeholder':'Подтверждение нового пароля'}))

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        user = self.user
        if user.check_password(current_password):
            return current_password
        else:
            raise forms.ValidationError('Текущий пароль не совпадает с паролем пользователя!')