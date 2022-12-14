from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class Faculty(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=200, null=False)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Список факультетов'
        ordering = ['name']

    def __str__(self):
        return self.name

class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=200, null=False)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Список кафедр'
        ordering = ['name']

    def __str__(self):
        return self.name

class Specialty(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=200, null=False)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Справочник специальностей'
        ordering = ['name']

    def __str__(self):
        return self.code + '. ' + self.name

class Subject(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=200, null=False)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Справочник дисциплин'
        ordering = ['name']

    def __str__(self):
        return self.name

class AcademicDegree(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=200, null=False)

    class Meta:
        verbose_name = 'Ученая степень'
        verbose_name_plural = 'Справочник ученых степеней'
        ordering = ['name']

    def __str__(self):
        return self.name

class AcademicTitle(models.Model):
    name = models.CharField(max_length=200, null=False)

    class Meta:
        verbose_name = 'Звание преподавателя'
        verbose_name_plural = 'Справочник званий преподавателей'
        ordering = ['name']

    def __str__(self):
        return self.name

class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    academic_degree = models.ForeignKey(AcademicDegree, on_delete=models.SET_NULL, blank=True, null=True)
    academic_title = models.ForeignKey(AcademicTitle, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Научный руководитель'
        verbose_name_plural = 'Научные руководители'
        ordering = ['id']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh_from_db()
        group, _created = Group.objects.get_or_create(name='Supervisors')
        self.user.groups.add(group)

    def __str__(self):
        if self.user.last_name:
            return self.user.last_name
        else:
            return self.user.username

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = 'Администрация - представитель'
        verbose_name_plural = 'Администрация - представители'
        ordering = ['id']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh_from_db()
        group, _created = Group.objects.get_or_create(name='Administration')
        self.user.groups.add(group)

    def __str__(self):
        return str(self.id) + ' ' + self.user.last_name