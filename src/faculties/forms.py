from django import forms

from .models import Supervisor

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ('department', 'academic_degree', 'academic_title')

        labels = {
            'department': 'Кафедра:', 
            'academic_degree': 'Ученая степень:', 
            'academic_title': 'Ученое звание:'
        }
