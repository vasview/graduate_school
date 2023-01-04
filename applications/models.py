from email.policy import default
import imp
from django.db import models
from django.contrib.auth.models import User

from postgraduates.models import EducationType
from faculties.models import Specialty

class ApplicationStatus(models.IntegerChoices):
    NEW = 1, 'новое' 
    APPROVED = 5, 'одобрено'
    REJECTED = 10, 'отказано'

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    form_of_study = models.CharField(
        max_length=2,
        choices=EducationType.choices,
        default=EducationType.NONE,
    )
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT)
    number_of_years = models.SmallIntegerField(blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    status = models.IntegerField(choices=ApplicationStatus.choices, default=ApplicationStatus.NEW)
    is_terms_accepted = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заявления'
        verbose_name_plural = 'Список заявлений'
        ordering = ['application_date', 'id']

    def __str__(self):
        return str(self.id)
