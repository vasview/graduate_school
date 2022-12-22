from django import forms
from django.forms.widgets import DateInput
from tinymce.widgets import TinyMCE

from .models import DissertationTopic, ExplanatoryNote

class EditDissertationTopic(forms.ModelForm):
    class Meta:
        model = DissertationTopic

        fields = ['name','approved_by','approval_date','protocol_number']

        # name = forms.CharField(widget=TinyMCE(attrs={'class': 'form-control', 'rows': 3}))

        labels = {'name': 'Тема', 
                'approved_by': 'Кем утверждена:', 'approval_date':'Дата утверждения:', 
                'protocol_number': 'Номер протокола:'
        }
        
        widgets = {
            'name': TinyMCE(attrs={ 'class': 'form-control', 'rows':'10', 'required': "true" }),
            'approved_by': forms.TextInput(attrs={ 'class': 'form-control' }),
            'protocol_number': forms.TextInput(attrs={ 'class': 'form-control' }),
            'approval_date': DateInput(attrs={ 'type': 'date', 'class': 'form-control' })
        }

class EditExplanatoryNote(forms.ModelForm):
    class Meta:
        model = ExplanatoryNote

        fields = ['topicality', 'purpose', 'scientific_value', 'expected_result', 'application_area',
                'topic_approval_status', 'purpose_approval_status', 'value_approval_status',
                'result_approval_status', 'application_approval_status']

        labels = {'topicality': 'Актуальность темы', 
                'purpose': 'Основная цель и задачи диссертации:', 
                'scientific_value':'Новизна и научная значимость диссертации:', 
                'expected_result': 'Ожидаемые результаты:',
                'application_area': 'Область применения:'
        }

        widgets = {
            'topicality': TinyMCE(attrs={ 'class': 'form-control', 'rows':'10', 'required': "true" }),
            'purpose': TinyMCE(attrs={ 'class': 'form-control', 'rows':'10',}),
            'scientific_value': TinyMCE(attrs={ 'class': 'form-control', 'rows':'10', }),
            'expected_result': TinyMCE(attrs={ 'class': 'form-control', 'rows':'10', }),
            'application_area': TinyMCE(attrs={ 'class': 'form-control', 'rows':'10', }),  
        }

        def clean_topic_approval_status(self):
            return self.initial['topic_approval_status']

        def clean_purpose_approval_status(self):
            return self.initial['purpose_approval_status']

        def clean_value_approval_status(self):
            return self.initial['value_approval_status']

        def clean_result_approval_status(self):
            return self.initial['result_approval_status']

        def clean_application_approval_status(self):
            return self.initial['application_approval_status']
