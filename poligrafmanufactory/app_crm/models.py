from django.db import models


class Counterparty(models.Model):
    title = models.CharField('Наименование', max_length=200)
    is_client = models.BooleanField('Является клиентом', default=False)
    is_provider = models.BooleanField('Является поставщиком', default=False)

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'

    def __str__(self):
        return self.title


class Order(models.Model):
    number = models.CharField('Номер', max_length=20)
    date = models.DateTimeField('Дата')
    client = models.ForeignKey(Counterparty, verbose_name='Клиент', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        unique_together = ('number', 'date')

    def __str__(self):
        return f'Заказ №{self.number} от {self.date}'
