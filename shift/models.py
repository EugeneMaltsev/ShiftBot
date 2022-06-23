from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


class User(AbstractUser):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email']


class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.CharField(max_length=128)
    technical_requirement = models.TextField()
    customer = models.CharField(max_length=64, blank=True)
    customer_email = models.EmailField(blank=True)
    start = models.DateField()
    hourly_rate = models.FloatField()
    bill = models.FloatField(blank=True, default=0)
    duration = models.DurationField(blank=True, default=datetime.timedelta(0))

    def __str__(self):
        return f'{self.owner.username} | {self.task}'


class Shift(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField(blank=True, null=True)
    wage = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.project.owner.first_name} {self.project.owner.last_name}' \
               f' | {self.start_time.date()} | {self.start_time.time()} - {self.end_time.time()}'
