from django.db import models

class ApplicationParameters(models.Model):
    code = models.CharField(max_length=100, blank=False, unique=True)
    name = models.CharField(max_length=250, blank=False)
    value = models.CharField(max_length=250, blank=False)

    class  Meta:
        verbose_name = 'Параметр приложения'
        verbose_name_plural = 'Параметры приложения'
        ordering = ['id']

    def __str__(self):
        return self.name

class MenuShownOnPages(models.IntegerChoices):
    POSTGRADUATE    = 1, 'аспирант' 
    SUPERVISOR      = 2, 'руководитель'
    ADMINISTRATION  = 3, 'администрация'


class MenuItems(models.Model):
    title = models.CharField(max_length=50, blank=False)
    url_name = models.CharField(max_length=250, blank=False)
    sort = models.SmallIntegerField()
    seen_by = models.IntegerField(choices=MenuShownOnPages.choices, default=MenuShownOnPages.POSTGRADUATE)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['seen_by', 'sort']

    def __str__(self):
        return self.get_seen_by_display().upper() + ' : ' + self.title

