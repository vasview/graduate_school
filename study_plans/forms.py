from django import forms

from .models import StudyPlanType

class NewStudyPlan(forms.Form):
    study_plan_type = forms.ModelChoiceField(
        required=True,
        queryset=StudyPlanType.objects.all(),
    )