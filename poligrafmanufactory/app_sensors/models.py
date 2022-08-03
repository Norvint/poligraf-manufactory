from django.db import models

from app_working_centers.models import WorkingCenterNode


class TypeOfSensor(models.Model):
    title = models.CharField('Наименование', max_length=100)

    class Meta:
        verbose_name = 'Тип датчика'
        verbose_name_plural = 'Типы датчиков'

    def __str__(self):
        return self.title


class Sensor(models.Model):
    title = models.CharField('Наименование', max_length=100)
    node_of_work_center = models.ForeignKey(WorkingCenterNode, on_delete=models.CASCADE,
                                            verbose_name='Узел рабочего центра')
    type_of_sensor = models.ForeignKey(TypeOfSensor, on_delete=models.CASCADE, verbose_name='Тип датчика')

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'

    def __str__(self):
        return f'{self.title} - {self.node_of_work_center}'
