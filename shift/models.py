from django.conf import settings
# from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


class User(AbstractUser):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email']


class Project(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    task = models.CharField(max_length=128)
    technical_requirement = models.TextField()
    customer = models.CharField(max_length=64, blank=True)
    customer_email = models.EmailField(blank=True)
    start_of_the_project = models.DateField()
    salary_per_hour = models.FloatField()
    project_cost = models.FloatField(blank=True, default=0)
    project_duration = models.DurationField(blank=True, default=datetime.timedelta(0))

    def __str__(self):
        return f'{self.user.username} | {self.task}'


class Shift(models.Model):
    user_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    shift_start_time = models.DateTimeField()
    shift_end_time = models.DateTimeField()
    shift_duration_time = models.DurationField(blank=True, null=True)
    salary_per_shift = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.user_project.user.first_name} {self.user_project.user.last_name}' \
               f' | {self.shift_start_time.date()} | {self.shift_start_time.time()} - {self.shift_end_time.time()}'

# TODO: fix 'get_user_model()'
