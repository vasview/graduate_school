from django import forms
from django.forms.widgets import DateInput

from .models import DissertationTopic, ExplanatoryNote

class EditDissertationTopic(forms.ModelForm):
    class Meta:
        model = DissertationTopic

        fields = ['name','approved_by','approval_date','protocol_number']

        labels = {'name': 'Тема', 
                'approved_by': 'Кем утверждена:', 'approval_date':'Дата утверждения:', 
                'protocol_number': 'Номер протокола:'
        }
        
        widgets = {
            'name': forms.Textarea(attrs={ 'class': 'form-control', 'rows':'3', 'required': "true" }),
            'approved_by': forms.TextInput(attrs={ 'class': 'form-control' }),
            'protocol_number': forms.TextInput(attrs={ 'class': 'form-control' }),
            'approval_date': DateInput(attrs={ 'type': 'date', 'class': 'form-control' })
        }

class EditExplanatoryNote(forms.ModelForm):
    class Meta:
        model = ExplanatoryNote

        fields = ['topicality', 'purpose', 'scientific_value', 'expected_result', 'application_area']

        labels = {'topicality': 'Актуальность темы', 
                'purpose': 'Основная цель и задачи диссертации:', 
                'scientific_value':'Новизна и научная значимость диссертации:', 
                'expected_result': 'Ожидаемые результаты:',
                'application_area': 'Область применения:'
        }
        
        widgets = {
            'topicality': forms.Textarea(attrs={ 'class': 'form-control', 'rows':'3', 'required': "true" }),
            'purpose': forms.Textarea(attrs={ 'class': 'form-control', 'rows':'3',}),
            'scientific_value': forms.Textarea(attrs={ 'class': 'form-control', 'rows':'3', }),
            'expected_result': forms.Textarea(attrs={ 'class': 'form-control', 'rows':'3', }),
            'application_area': forms.Textarea(attrs={ 'class': 'form-control', 'rows':'3', }),  
        }
