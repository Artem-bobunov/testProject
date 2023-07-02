from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('создана', 'Создана'),
        ('в обработке', 'В обработке'),
        ('ответ', 'Ответ'),
    ]
    numberTask = models.IntegerField('Номер задачи',null=True,blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='создана')

