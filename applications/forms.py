import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from postgraduates.models import EducationType
from faculties.models import Specialty
from profiles.models import Country, Gender, Education

class NewApplicationForm(forms.Form):
    application_date = forms.DateField(initial=datetime.date.today)
    number_of_years = forms.IntegerField(max_value=4, min_value=1)
    specialty = forms.ModelChoiceField(
        required=True,
        queryset=Specialty.objects.all(),
        empty_label='Выберите специальность',
    )
    form_of_study = forms.ChoiceField(
        required=True,
        choices=EducationType.choices,
    )
    first_name = forms.CharField(max_length=150)
    middle_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150)
    email = forms.CharField(max_length=254)
    birth_date = forms.DateField()
    citizenship = forms.ModelChoiceField(
        required=True,
        queryset=Country.objects.all(),
        empty_label='Выберите страну',
    )
    gender = forms.ChoiceField(
        required=True,
        choices=Gender.choices
    )
    document_name = forms.CharField(max_length=50)
    document_code = forms.CharField(max_length=10)
    document_number = forms.CharField(max_length=10)
    issued_by = forms.CharField(max_length=50)
    issue_date = forms.DateField()
    personal_number = forms.CharField(max_length=20)
    birthdate_place = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    diploma_number = forms.CharField(max_length=50)
    diploma_issued = forms.DateField()
    edu_organization = forms.CharField(max_length=200)
    education_level = forms.ModelChoiceField(
        required=True,
        queryset = Education.objects.all(),
        empty_label='Выберите уровень',
    )
    is_terms_accepted = forms.BooleanField()

    def clean_application_date(self):
        data = self.cleaned_data['application_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - Application Date in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - Application Date is more than 4 weeks ahead'))

        return data


class UpdateApplicationForm(forms.Form):
    pass

class AllApplicationsForm(forms.Form):
    pass