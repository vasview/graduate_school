from io import open_code
from tokenize import blank_re
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

class Gender(models.TextChoices):
    NONE = 'NA', 'Не задано'
    MALE = 'M', 'Мужчина'
    FEMALE = 'F', 'Женщина'

class Education(models.Model):
    code = models.CharField(max_length=10, blank=False)
    name = models.CharField(max_length=50, blank=False)

    class Meta:
        verbose_name = 'Уровень образования'
        verbose_name_plural = 'Уровни образования'
        ordering = ['name']

    def __str__(self):
        return self.name

class Country(models.Model):
    code = models.CharField(max_length=10, blank=False)
    name = models.CharField(max_length=50, blank=False)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Справочник стран'
        ordering = ['name']

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    mobile = PhoneNumberField(blank=True, null=True)
    personal_number = models.CharField(blank=True, null=True, max_length=20)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=2,
        choices=Gender.choices,
        default=Gender.NONE,
    )

class ContactDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=50, blank=False)
    document_code = models.CharField(max_length=10, blank=False)
    document_number = models.CharField(max_length=10, blank=False)
    issue_date = models.DateField(blank=False)
    issued_by = models.CharField(max_length=50, blank=False)
    birthdate_place = models.CharField(max_length=100, blank=False)
    education_level = models.ForeignKey(Education, on_delete=models.SET_NULL, blank=True, null=True)
    citizenship = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)

class EducationalDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educational_documents')
    number = models.CharField(max_length=50, blank=False)
    issued_date = models.DateField(blank=False)
    organization = models.CharField(max_length=200, blank=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
