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
