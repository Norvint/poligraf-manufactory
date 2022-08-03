import os

from django.db import models


class WorkingCenter(models.Model):
    title = models.CharField('Название', max_length=100)
    image = models.ImageField('Изображение', upload_to=os.path.join('app_working_centers', 'work_centers'))

    class Meta:
        verbose_name = 'Рабочий центр'
        verbose_name_plural = 'Рабочие центры'

    def __str__(self):
        return self.title


class WorkingCenterNode(models.Model):
    title = models.CharField('Название', max_length=100)
    image = models.ImageField('Изображение', null=True, blank=True,
                              upload_to=os.path.join('app_working_centers', 'nodes'))
    work_center = models.ForeignKey(WorkingCenter, on_delete=models.CASCADE, verbose_name='Рабочий центр')

    class Meta:
        verbose_name = 'Узел рабочего центра'
        verbose_name_plural = 'Узлы рабочих центров'

    def __str__(self):
        return f'{self.title} ({self.work_center})'
