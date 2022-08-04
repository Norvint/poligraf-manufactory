from django.db import models

from app_working_centers.models import WorkingCenterNode


class InterfaceAdapter(models.Model):
    ADAPTER_TYPES = [
        ('tcp', 'rs485/eth'),
        ('serial', 'rs485/usb'),
    ]

    title = models.CharField('Название', max_length=200)
    address = models.CharField('Адрес', max_length=100)
    port = models.IntegerField('Порт')
    type = models.CharField('Тип адаптера', choices=ADAPTER_TYPES, max_length=100)

    class Meta:
        verbose_name = 'Адаптер интерфейса'
        verbose_name_plural = 'Адаптеры интерфейсов'

    def __str__(self):
        return self.title


class TypeOfDevice(models.Model):
    title = models.CharField('Наименование', max_length=100)

    class Meta:
        verbose_name = 'Тип устройства'
        verbose_name_plural = 'Типы устройств'

    def __str__(self):
        return self.title


class Device(models.Model):
    title = models.CharField('Наименование', max_length=100)
    address = models.PositiveIntegerField('Адрес')
    type_of_device = models.ForeignKey(TypeOfDevice, on_delete=models.CASCADE, verbose_name='Тип устройства')
    node_of_work_center = models.ForeignKey(WorkingCenterNode, on_delete=models.CASCADE,
                                            verbose_name='Узел рабочего центра')
    interface_adapter = models.OneToOneField(InterfaceAdapter,
                                             on_delete=models.PROTECT,
                                             verbose_name='Адаптер интерфейса')

    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'

    def __str__(self):
        return f'{self.title} - {self.node_of_work_center}'


class ParameterType(models.Model):
    title = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Тип параметра'
        verbose_name_plural = 'Типы параметров'

    def __str__(self):
        functions = ''
        for available_function in AvailableFunctions.objects.filter(parameter_type=self.pk):
            functions += available_function.code + ' '
        return f'{self.title} ({functions})'


class AvailableFunctions(models.Model):
    title = models.CharField('Название', max_length=100)
    code = models.CharField('Код', max_length=10)
    parameter_type = models.ForeignKey(ParameterType, on_delete=models.CASCADE, verbose_name='Тип параметра')

    class Meta:
        verbose_name = 'Доступная функция'
        verbose_name_plural = 'Доступные функции'

    def __str__(self):
        return f'{self.code} ({self.title})'


class DeviceParameter(models.Model):
    DATA_FORMATS = [
        ('LONG', 'LONG'),
        ('ASCII', 'ASCII'),
        ('WORD', 'WORD'),
        ('DWORD', 'DWORD'),
        ('BYTE', 'BYTE')
    ]

    title = models.CharField('Название', max_length=200)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройство')
    address = models.PositiveIntegerField('Адрес')
    parameter_type = models.ForeignKey(ParameterType, on_delete=models.CASCADE, verbose_name='Тип параметра')
    format = models.CharField('Формат данных', max_length=100, choices=DATA_FORMATS)

    class Meta:
        verbose_name = 'Параметр устройства'
        verbose_name_plural = 'Параметры устройств'

    def __str__(self):
        return f'{self.pk}. {self.title} ({self.device})'
