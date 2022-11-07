from hashlib import blake2b
from tabnanny import verbose
from django.db import models

class ReferenceTable(models.IntegerChoices):
    NONE = 0
    EXAMS = 1 , 'postgraduates.exam'
    SUBJECTS = 2 , 'faculties.subject'

class StudyPlanType(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    sort = models.SmallIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Тип учебного плана аспиранта'
        verbose_name_plural = '1.Справочник учебных планов - Типы учебных планов аспиранта'
        ordering = ['sort']

    def __str__(self):
        return self.name

class Work(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    sort = models.SmallIntegerField()
    active = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    genplan_visible = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Наименование работы'
        verbose_name_plural = '2.Справочник учебных планов - Наименования работ учебного плана'
        ordering = ['title']

    def __str__(self):
        return self.title

class WorkScope(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    sort = models.SmallIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Объем работы'
        verbose_name_plural = '3.Справочник учебных планов - Наименование объемов работ'
        ordering = ['title']

    def __str__(self):
        return self.title

class StudyPlan(models.Model):
    postgraduate = models.ForeignKey('postgraduates.Postgraduate', on_delete=models.PROTECT)
    work = models.ForeignKey(Work, on_delete=models.PROTECT)
    year_of_study = models.SmallIntegerField()
    plan_type = models.ForeignKey(StudyPlanType, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Учебный план заголовок'
        verbose_name_plural = 'Учебные планы - заголовки'
        ordering = ['id']

    def __str__(self):
        return self.postgraduate.student.last_name

class StudyWork(models.Model):
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.PROTECT)
    work_scope = models.ForeignKey(WorkScope, on_delete=models.PROTECT)
    subtitle = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_section_title = models.BooleanField(default=False)

class StudyWorkDetails(models.Model):
    study_work = models.ForeignKey(StudyWork, on_delete=models.PROTECT)
    reference_table = models.SmallIntegerField(choices=ReferenceTable.choices, 
                                               default=ReferenceTable.NONE)
    reference_key = models.IntegerField(blank=True, null=True)
    deadline = models.DateField()
    reporting_form = models.CharField(max_length=250, blank=True, null=True)
    completion_mark = models.CharField(max_length=100, blank=True, null=True)
    faculty_conclustion = models.TextField(blank=True, null=True)
