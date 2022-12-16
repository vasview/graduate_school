from email.policy import default
from secrets import choice
from tabnanny import verbose
from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User

class EducationType(models.TextChoices):
    NONE = 'NA', 'Не выбрано'
    FULLTIME = 'FT', 'Очное'
    DISTANCE = 'DL', 'Заочное'

class ExamGrade(models.IntegerChoices):
    NONE = -1, 'не выставлено' 
    PASSED = 0, 'зачет'
    UNSATISFACTORY = 2, 'неудовлетворительно'
    SATISFACTORY = 3, 'удовлетворительно'
    GOOD = 4, 'хорошо'
    EXCELLENT = 5, 'отлично'

class ExplanatoryNoteSectionStatus(models.IntegerChoices):
    NEW = 1, 'не проверено' 
    REWORK = 3, 'доработка'
    APPROVED = 5, 'утверждено'

class Postgraduate(models.Model):
    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='students')
    department = models.ForeignKey('faculties.Department', on_delete=models.SET_NULL, blank=True, null=True)
    specialty = models.ForeignKey('faculties.Specialty', on_delete=models.SET_NULL, blank=True, null=True)
    supervisor = models.ForeignKey('faculties.Supervisor', on_delete=models.SET_NULL, blank=True, null=True)
    form_of_study = models.CharField(
        max_length=2,
        choices=EducationType.choices,
        default=EducationType.NONE,
    )
    number_of_years = models.SmallIntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    expected_end_date = models.DateField(blank=True, null=True)
    real_end_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Аспирант'
        verbose_name_plural = 'Аспиранты'
        ordering = ['id']

    def __str__(self):
        return self.student.last_name

class DissertationTopic(models.Model):
    postgraduate = models.ForeignKey(Postgraduate, on_delete=models.PROTECT, related_name='topics')
    name = models.TextField()
    approved_by = models.CharField(max_length=250, blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    protocol_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Тема диссертации'
        verbose_name_plural = 'Темы диссертации'
        ordering = ['id']

    def __str__(self):
        return self.id


class ExplanatoryNote(models.Model):
    postgraduate = models.ForeignKey(Postgraduate, on_delete=models.CASCADE, related_name='explanatory_notes')
    topicality = models.TextField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    scientific_value = models.TextField(blank=True, null=True)
    expected_result = models.TextField(blank=True, null=True)
    application_area = models.TextField(blank=True, null=True)
    topic_approval_status = models.IntegerField(choices=ExplanatoryNoteSectionStatus.choices, 
                                                default=ExplanatoryNoteSectionStatus.NEW)
    purpose_approval_status = models.IntegerField(choices=ExplanatoryNoteSectionStatus.choices, 
                                                default=ExplanatoryNoteSectionStatus.NEW)
    value_approval_status = models.IntegerField(choices=ExplanatoryNoteSectionStatus.choices, 
                                                default=ExplanatoryNoteSectionStatus.NEW)
    result_approval_status = models.IntegerField(choices=ExplanatoryNoteSectionStatus.choices, 
                                                default=ExplanatoryNoteSectionStatus.NEW)
    application_approval_status = models.IntegerField(choices=ExplanatoryNoteSectionStatus.choices, 
                                                default=ExplanatoryNoteSectionStatus.NEW)

    def info_status_css(self, section_status):
        """
        helper method for a css class used in template depending on the approval status
        """
        if section_status == 1:
            return 'status_info_primary'
        elif section_status == 3:
            return 'status_info_warning'
        else:
            return 'status_info_success'

    def __str__(self):
        return self.id

class Exam(models.Model):
    postgraduate = models.ForeignKey(Postgraduate, on_delete=models.PROTECT)
    subject = models.ForeignKey('faculties.Subject', on_delete=models.PROTECT)
    date = models.DateField(blank=True, null=True)
    is_candidate_exam = models.BooleanField(default=False)
    mark = models.IntegerField(choices=ExamGrade.choices, default=ExamGrade.NONE)

    class Meta:
        verbose_name = 'Экзамен'
        verbose_name_plural = 'Экзамены'
        ordering = ['date']

    def __str__(self):
        return self.subject.name
