from django import forms

class LoginForm(forms.Form):
    user = forms.CharField(max_length=50, label='Пользователь', 
                        widget=forms.TextInput(attrs={'class':'form-control', 'id':"user", 'placeholder':'Пользователь'}))
    password = forms.CharField(max_length=50, label='Пароль',
                        widget=forms.PasswordInput(attrs={'class':'form-control', 'id':"password", 'placeholder':'Пароль'}))