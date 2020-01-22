from django.db import models
from django.db.models import Sum, Max, Min


class User(models.Model):
    first_name = models.CharField('Фамилия пользователя', max_length=256)
    last_name = models.CharField('Имя пользователя', max_length=256)
    email = models.CharField('Почта пользователя', max_length=256)
    gender = models.CharField('Пол пользователя', max_length=256)
    ip_address = models.CharField('IP пользователя', max_length=256)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def total_clicks(self):
        return Statistic.objects.filter(user=self.id).aggregate(Sum('clicks'))['clicks__sum']

    def total_page_views(self):
        return Statistic.objects.filter(user=self.id).aggregate(Sum('page_views'))['page_views__sum']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Statistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('Дата')
    page_views = models.IntegerField()
    clicks = models.IntegerField()

    def __str__(self):
        return f'User name: {self.user.first_name} {self.user.last_name}'

    @classmethod
    def get_start_date(cls, user_id):
        return cls.objects.filter(user=user_id).aggregate(Min('date'))['date__min']

    @classmethod
    def get_end_date(cls, user_id):
        return cls.objects.filter(user=user_id).aggregate(Max('date'))['date__max']

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистики'
