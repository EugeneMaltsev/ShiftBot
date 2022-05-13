from django.conf import settings
# from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
import numpy as np
import pandas as pd
import datetime


# TODO: fix 'get_user_model()'


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

    def get_projects_statistics(self, query_set):
        df = pd.DataFrame(query_set)
        number_of_projects = df["id"].count()
        project_cost_summary = df["project_cost"].sum()
        project_cost_mean = df["project_cost"].mean()
        project_duration_summary = df["project_duration"].sum() / np.timedelta64(1, 'h')
        project_duration_mean = df["project_duration"].mean() / np.timedelta64(1, 'h')
        statistics = [number_of_projects,
                      project_cost_summary,
                      project_duration_summary,
                      project_cost_mean,
                      project_duration_mean]
        return statistics

    def __str__(self):
        return f'{settings.AUTH_USER_MODEL.username} | {self.task}'


class Shift(models.Model):
    user_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    shift_start_time = models.DateTimeField()
    shift_end_time = models.DateTimeField()
    shift_duration_time = models.DurationField(blank=True, null=True)
    salary_per_shift = models.FloatField(blank=True, null=True)

    def calculate_shift_duration_time(self):
        self.shift_duration_time = self.shift_end_time - self.shift_start_time
        self.user_project.project_duration += self.shift_duration_time
        self.user_project.save()
        return self.shift_duration_time

    def calculate_salary_per_shift(self):
        self.salary_per_shift = (self.shift_duration_time.seconds / 3600) * self.user_project.salary_per_hour
        self.user_project.project_cost += self.salary_per_shift
        self.user_project.save()
        return self.salary_per_shift

    def get_shift_statistics(self, query_set):
        df = pd.DataFrame(query_set)
        number_of_shifts = df["id"].count()
        number_of_hours = df["shift_duration_time"].sum() / np.timedelta64(1, 'h')
        duration_mean = df["shift_duration_time"].mean() / np.timedelta64(1, 'h')
        salary_mean = df["salary_per_shift"].mean()
        statistics = [number_of_shifts,
                      number_of_hours,
                      self.user_project.project_cost,
                      duration_mean,
                      salary_mean]
        return statistics

    def __str__(self):
        return f'{self.user_project.user} {self.user_project.user.last_name}' \
               f' | {self.shift_start_time.date()} | {self.shift_start_time.time()} - {self.shift_end_time.time()}'
