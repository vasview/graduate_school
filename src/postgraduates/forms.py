from django import forms
from django.forms.widgets import DateInput
from tinymce.widgets import TinyMCE

from .models import DissertationTopic, ExplanatoryNoteSection

class EditDissertationTopicForm(forms.ModelForm):
    class Meta:
        model = DissertationTopic

        fields = ['name','approved_by','approval_date','protocol_number']

        # name = forms.CharField(widget=TinyMCE(attrs={'class': 'form-control', 'rows': 3}))

        labels = {'name': 'Тема', 
                'approved_by': 'Кем утверждена:', 'approval_date':'Дата утверждения:', 
                'protocol_number': 'Номер протокола:'
        }
        
        widgets = {
            'name': TinyMCE(attrs={ 'class': 'form-control', 'rows':'15' }),
            'approved_by': forms.TextInput(attrs={ 'class': 'form-control'  }),
            'protocol_number': forms.TextInput(attrs={ 'class': 'form-control'  }),
            'approval_date': DateInput(attrs={ 'type': 'date', 'class': 'form-control' })
        }

class ExplanatorySectionForm(forms.ModelForm):
    class Meta:
        model = ExplanatoryNoteSection

        fields = ['postgraduate', 'title', 'content', 'sort', 'is_custom']

        labels = {'title': 'Заголовок раздела:', 
                'content': 'Содержание:', 
                'sort':'Положение в документе:'
        }

        widgets = {
            'title': forms.TextInput(attrs={ 'class': 'form-control', 'required': "true" }),
            'content': TinyMCE(attrs={ 'class': 'form-control', 'rows':'15' }),
            'sort': forms.NumberInput(attrs={ 'class': 'form-control', 'type': 'number', 'min':'1', 'max':'20', 'required': "true" })
        }

class NewExplanatorySectionForm(ExplanatorySectionForm):
    class Meta(ExplanatorySectionForm.Meta):
        exclude = ('postgraduate', 'is_custom',)

class EditExplanatorySectionForm(ExplanatorySectionForm):
    class Meta(ExplanatorySectionForm.Meta):
        exclude = ('postgraduate',)
