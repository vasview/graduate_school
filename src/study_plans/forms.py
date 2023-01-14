from django import forms
from django.forms.widgets import DateInput

from .models import StudyPlanType, StudyPlan, StudyWorkScope, StudyWorkScopeDetails
from postgraduates.models import Postgraduate
from faculties.models import Subject

class NewStudyPlan(forms.ModelForm):
    class Meta:
        model = StudyPlan

        fields = ['postgraduate', 'plan_type']

    plan_type = forms.ModelChoiceField(
        required=True,
        queryset=StudyPlanType.objects.all(),
        empty_label='Учебный план не выбран'
    )

    def __init__(self, *args, **kwargs):
        self.postgraduate = kwargs.pop('postgraduate')
        super(NewStudyPlan, self).__init__(*args, **kwargs)

    # def save(self):
    #     data = self.cleaned_data
    #     # postgraduate = Postgraduate.objects.get(pk=data['postgraduate'])
    #     study_plan = StudyPlan(postgraduate=self.postgraduate,
    #                             plan_type=data['study_plan_type'])
    #     study_plan.save()
    #     return study_plan

class StudyPlanScopeDetailsCommonForm(forms.ModelForm):
    class Meta:
        model = StudyWorkScopeDetails
        fields = ['study_work_scope', 'subtitle', 'summary', 'subject', 'deadline', 'reporting_form']

        labels = {'subtitle': 'Заголовок:', 
                'summary': 'Краткое содержание:', 
                'subject': 'Дисциплина:',
                'deadline': 'Срок выполнения:',
                'reporting_form': 'Форма отчетности:'
        }

        subtitle = forms.CharField(min_length=1, max_length=250, required=False, 
                        widget=forms.TextInput()
        )
        summary = forms.CharField(required=False,
                        widget=forms.Textarea(attrs={ 'class': 'form-control', 'rows':'3', })
        )
        deadline = forms.DateField(required=True,
                        widget=DateInput(attrs={ 'type': 'date', 'class': 'form-control' })
        )
        reporting_form = forms.CharField(max_length=250, required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        subject = forms.ModelChoiceField(
            required=True,
            queryset=Subject.objects.all(),
            empty_label='Дисциплина не выбрана'
        )

class StudyPlanScopeDetailsForm(StudyPlanScopeDetailsCommonForm):
    class Meta(StudyPlanScopeDetailsCommonForm.Meta):
        exclude = ('subject',)

    def __init__(self, *args, **kwargs):
        self.study_work_scope = kwargs.pop('study_work_scope')
        super(StudyPlanScopeDetailsForm, self).__init__(*args, **kwargs)

class StudyPlanSubjectDetailsForm(StudyPlanScopeDetailsCommonForm):
    class Meta(StudyPlanScopeDetailsCommonForm.Meta):
        exclude = ('subtitle', 'summary', )

    def __init__(self, *args, **kwargs):
        self.study_work_scope = kwargs.pop('study_work_scope')
        super(StudyPlanSubjectDetailsForm, self).__init__(*args, **kwargs)
        self.fields['subject'].empty_label = 'Дисциплина не выбрана' 

class EditStudyPlanScopeDetailsForm(StudyPlanScopeDetailsCommonForm):
    class Meta(StudyPlanScopeDetailsCommonForm.Meta):
        exclude = ('subject',)

class EditStudyPlanSubjectDetailsForm(StudyPlanScopeDetailsCommonForm):
    class Meta(StudyPlanScopeDetailsCommonForm.Meta):
        exclude = ('subtitle', 'summary', )
