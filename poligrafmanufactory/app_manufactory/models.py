from django.db import models


class WorkCenter(models.Model):
    title = models.CharField('Название', max_length=200)

    class Meta:
        verbose_name = 'Рабочий центр'
        verbose_name_plural = "Рабочие центры"

    def __str__(self):
        return self.title
