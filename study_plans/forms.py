from django import forms

from .models import StudyPlanType, StudyPlan, WorkType
from postgraduates.models import Postgraduate

class NewStudyPlan(forms.Form):
    class Meta:
        model = StudyPlan

        fields = ['postgratude', 'study_plan_type']

    postgraduate = forms.IntegerField()
    study_plan_type = forms.ModelChoiceField(
        required=True,
        queryset=StudyPlanType.objects.all(),
    )

    def save(self):
        data = self.cleaned_data
        postgraduate = Postgraduate.objects.get(pk=data['postgraduate'])
        study_plan = StudyPlan(postgraduate=postgraduate,
                                plan_type=data['study_plan_type'])
        study_plan.save()
        return study_plan