from django.db import models

from app_crm.models import Counterparty, Order


class Shipment(models.Model):
    number = models.CharField('Номер', max_length=30)
    date = models.DateTimeField('Дата документа')
    name = models.CharField('Наименование документа', max_length=50)
    actual_date = models.DateTimeField('Фактическая дата отгрузки')
    planned_date = models.DateTimeField('Плановая дата отгрузки')
    shipped = models.BooleanField('Отгружен', default=False)
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.PROTECT)
    order_is_ready = models.BooleanField('Заказ готов', default=False)

    class Meta:
        verbose_name = 'Отгрузка'
        verbose_name_plural = 'Отгрузки'
        unique_together = ('number', 'date', 'name')

    def __str__(self):
        return f'{self.name} №{self.number} от {self.date}'


class Loading(models.Model):
    number = models.CharField('Номер', max_length=30)
    date = models.DateTimeField('Дата документа')
    name = models.CharField('Наименование документа', max_length=50)
    actual_date = models.DateTimeField('Фактическая дата приемки')
    planned_date = models.DateTimeField('Плановая дата приемки')
    loaded = models.BooleanField('Принят', default=False)
    provider = models.ForeignKey(Counterparty, verbose_name='Поставщик', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Приемка'
        verbose_name_plural = 'Приемки'
        unique_together = ('number', 'date', 'name')

    def __str__(self):
        return f'{self.name} №{self.number} от {self.date}'
