from django.forms.widgets import DateInput, EmailInput, NumberInput
import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from postgraduates.models import EducationType
from faculties.models import Specialty
from profiles.models import Country, Gender, Education, Profile, ContactDetails, EducationalDocument
from .models import Application

class NewApplicationForm(forms.Form):
    application_date = forms.DateField(initial=datetime.date.today, widget=NumberInput(attrs={'type': 'date'}))
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
    birth_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
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
    issue_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    personal_number = forms.CharField(max_length=20)
    birthdate_place = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    diploma_number = forms.CharField(max_length=50)
    diploma_issued = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
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

    def save(self):
        data = self.cleaned_data
        user = User(email=data['email'], username = data['email'],
            # username = data['first_name'] + '.' + data['last_name'],
            first_name=data['first_name'], last_name=data['last_name'],
            is_active=False)
        user.save()

        user.profile.middle_name=data['middle_name']
        user.profile.birth_date=data['birth_date']
        user.profile.mobile=data['mobile']
        user.profile.personal_number=data['personal_number']
        user.profile.gender=data['gender']
        user.save()

        user_details = ContactDetails(user=user, document_name=data['document_name'], 
            document_code=data['document_code'], document_number=data['document_number'], 
            issue_date=data['issue_date'], issued_by=data['issued_by'],
            birthdate_place=data['birthdate_place'], education_level=data['education_level'], 
            citizenship=data['citizenship'])
        user_details.save()

        user_edu_document = EducationalDocument(user=user, number=data['diploma_number'], 
            issued_date=data['diploma_issued'], organization=data['edu_organization'])
        user_edu_document.save()

        user_application = Application(user=user, application_date=data['application_date'], 
            form_of_study=data['form_of_study'], specialty=data['specialty'], 
            number_of_years=data['number_of_years'], is_terms_accepted=data['is_terms_accepted'])
        user_application.save()
