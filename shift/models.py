from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=64, blank=True)
    position = models.CharField(max_length=64, blank=True)
    employment_date = models.DateField()
    dismiss_date = models.DateField(blank=True, null=True)
    paid_medical_leave = models.BooleanField()
    salary_per_month = models.FloatField()

    def __str__(self):
        return self.user.username


class Shift(models.Model):

    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    shift_start_time = models.DateTimeField()
    shift_end_time = models.DateTimeField()
    shift_duration_time = models.DurationField(blank=True, null=True)
    overtime = models.DurationField(blank=True, null=True)
    salary_per_shift = models.FloatField(blank=True, null=True)
    medical_leave = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_profile.user.first_name} {self.user_profile.user.last_name}' \
               f' | {self.shift_start_time.date()}/{self.shift_end_time.date()}'
