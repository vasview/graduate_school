from hashlib import blake2b
from tabnanny import verbose
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class StudyPlanStatus(models.IntegerChoices):
    NEW = 1, 'не проверен' 
    REWORK = 3, 'доработка'
    APPROVED = 5, 'утвержден'

# Register for types of study plans
class StudyPlanType(models.Model):
    title = models.CharField(max_length=250)
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    year_of_study = models.SmallIntegerField()
    sort = models.SmallIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Тип учебного плана аспиранта'
        verbose_name_plural = '1.Справочник учебных планов - Типы учебных планов аспиранта'
        ordering = ['sort']

    def __str__(self):
        return self.title

# Register for types of works in a study plan
class WorkType(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    sort = models.SmallIntegerField()
    active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    is_genplan_visible = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Наименование работы'
        verbose_name_plural = '2.Справочник учебных планов - Наименования работ учебного плана'
        ordering = ['sort']

    def __str__(self):
        return self.title

# Register for types of work scope for the work in a study plan
class WorkScopeType(models.Model):
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE, related_name='work_scope_types')
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    sort = models.SmallIntegerField()
    active = models.BooleanField(default=True)
    is_title_visible = models.BooleanField(default=True)
    code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Объем работы'
        verbose_name_plural = '3.Справочник учебных планов - Наименование объемов работ'
        ordering = ['id', 'sort', 'title']

    def __str__(self):
        return "%s: %s" % (self.work_type.title, self.title)

# Header of a study plan
class StudyPlan(models.Model):
    postgraduate = models.ForeignKey('postgraduates.Postgraduate', on_delete=models.PROTECT, related_name='study_plans')
    plan_type = models.ForeignKey(StudyPlanType, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.IntegerField(choices=StudyPlanStatus.choices, default=StudyPlanStatus.NEW)
    completion_percentage = models.IntegerField(validators=[
                MinValueValidator(0),
                MaxValueValidator(100)],
                default=0
    )

    class Meta:
        verbose_name = 'Учебный план заголовок'
        verbose_name_plural = 'Учебные планы - заголовки'
        ordering = ['id']

    def get_status_css(self):
        """
        helper method for a css class used in template depending on the approval status
        """
        if self.status == 1:
            return 'status_info_primary'
        elif self.status == 3:
            return 'status_info_warning'
        else:
            return 'status_info_success'

    def recalculate_completion_percentage(self):
        works = self.study_plan_works.all()
        completion_percentage = 0
        for work in works:
            completion_percentage += work.completion_percentage

        completion_percentage = int(round(completion_percentage / works.count()))
        self.completion_percentage = completion_percentage
        self.save(update_fields=['completion_percentage'])
        return self.completion_percentage

    def __str__(self):
        return self.postgraduate.student.last_name + ' ' + self.plan_type.title

    def get_absolute_url(self):
        return reverse('student_study_plans:show_study_plan', args=[self.id])

# Study plan with a work
class StudyPlanWork(models.Model):
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.PROTECT, related_name='study_plan_works')
    work_type = models.ForeignKey(WorkType, on_delete=models.PROTECT)
    completion_percentage = models.IntegerField(validators=[
                MinValueValidator(0),
                MaxValueValidator(100)],
                default=0
    )

    def left_percentage(self):
        return 100 - self.completion_percentage

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.work_type.title

# Work scope in the study plan
class StudyWorkScope(models.Model):
    study_plan_work = models.ForeignKey(StudyPlanWork, on_delete=models.PROTECT, related_name='study_work_scopes')
    work_scope = models.ForeignKey(WorkScopeType, on_delete=models.PROTECT)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.work_scope.title

# Details of a work scope in the study plan
class StudyWorkScopeDetails(models.Model):
    study_work_scope = models.ForeignKey(StudyWorkScope, on_delete=models.PROTECT, related_name='study_work_scope_details')
    subtitle = models.CharField(max_length=250, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    subject = models.ForeignKey('faculties.Subject', on_delete=models.SET_NULL, blank=True, null=True, related_name='study_work_subjects')
    deadline = models.DateField(blank=True, null=True)
    reporting_form = models.CharField(max_length=250, blank=True, null=True)
    completion_mark = models.CharField(max_length=100, blank=True, null=True)
    faculty_conclustion = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['id']
