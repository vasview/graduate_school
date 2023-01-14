from email.policy import default
from secrets import choice
from tabnanny import verbose
from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.utils.safestring import SafeString

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

# Register for types of sections in Explanatory note
class ExplanatoryNoteSectionType(models.Model):
    name = models.CharField(max_length=250)
    sort = models.SmallIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Раздел объяснительной записки'
        verbose_name_plural = '3.Справочник разделов объяснительной записки'
        ordering = ['sort']

    def __str__(self):
        return self.name

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
        verbose_name_plural = '1.Аспиранты'
        ordering = ['id']

    def __str__(self):
        return self.student.last_name

class DissertationTopic(models.Model):
    postgraduate = models.ForeignKey(Postgraduate, on_delete=models.PROTECT, related_name='topics')
    name = HTMLField(blank=True, null=True)
    approved_by = models.CharField(max_length=250, blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    protocol_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Тема диссертации'
        verbose_name_plural = '2.Темы диссертации'
        ordering = ['id']

    def __str__(self):
        return str(self.id) + ' ' + self.postgraduate.student.last_name

class ExplanatoryNoteSection(models.Model):
    postgraduate = models.ForeignKey(Postgraduate, on_delete=models.CASCADE, related_name='expl_note_sections')
    title = models.CharField(max_length=250, blank=True, null=True)
    content = HTMLField(blank=True, null=True)
    approval_status = models.IntegerField(choices=ExplanatoryNoteSectionStatus.choices, 
                                                default=ExplanatoryNoteSectionStatus.NEW)
    sort = models.IntegerField()
    is_custom = models.BooleanField(default=False)
    supervisor_comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['sort']

    def get_status_css(self):
        """ return a css class used in template depending on the approval status """
        if self.approval_status == 1:
            return 'status_info_primary'
        elif self.approval_status == 3:
            return 'status_info_warning'
        else:
            return 'status_info_success'

    def __str__(self):
        return self.title

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
