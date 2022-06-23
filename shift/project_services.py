from rest_framework.exceptions import ValidationError, NotFound
from shift.models import Shift, Project
import numpy as np
import pandas as pd


def shift_create(validated_data):
    shift = Shift()
    shift.project = validated_data['project']
    shift.start_time = validated_data['start_time']
    shift.end_time = validated_data['end_time']
    duration = calculate_shift_duration_time(shift)
    salary = calculate_salary_per_shift(shift)
    return Shift.objects.create(project_id=validated_data['project_id'],
                                shift_start_time=validated_data['start_time'],
                                shift_end_time=validated_data['end_time'],
                                shift_duration_time=duration,
                                salary_per_shift=salary)


def calculate_shift_duration_time(shift):
    shift.duration = shift.end_time - shift.start_time
    shift.project.duration += shift.duration
    shift.project.save()
    return shift.duration


def calculate_salary_per_shift(shift):
    shift.wage = (shift.duration.seconds / 3600) * shift.project.hourly_rate
    shift.project.bill += shift.wage
    shift.project.save()
    return shift.wage


def get_projects_statistics(queryset):
    df = pd.DataFrame(list(queryset.values()))
    number_of_projects = df['id'].count()
    project_cost_summary = df['bill'].sum()
    project_cost_mean = df['bill'].mean()
    project_duration_summary = df['duration'].sum() / np.timedelta64(1, 'h')
    project_duration_mean = df['duration'].mean() / np.timedelta64(1, 'h')
    statistics = ({
        'amount_of_projects': number_of_projects,
        'bill_summary': project_cost_summary,
        'bill_mean': project_cost_mean,
        'duration_summary': project_duration_summary,
        'duration_mean': project_duration_mean
    })
    return statistics


def get_shift_statistics(queryset):
    df = pd.DataFrame(list(queryset.values()))
    number_of_shifts = df['id'].count()
    number_of_hours = df['duration'].sum() / np.timedelta64(1, 'h')
    duration_mean = df['duration'].mean() / np.timedelta64(1, 'h')
    salary_mean = df['wage'].mean()
    statistics = ({
        'amount_of_shifts': number_of_shifts,
        'amount_of_hours': number_of_hours,
        'duration_mean': duration_mean,
        'wage_mean': salary_mean,
        'bill': queryset.first().project.bill,
    })
    return statistics


def all_shifts_by_project_queryset(request, queryset):
    try:
        if Project.objects.filter(owner=request.user).filter(id=request.data['project']).exists():
            if queryset.filter(project_id=request.data['project']).exists():
                return queryset.filter(project_id=request.data['project'])
            else:
                raise NotFound('There are no shifts in this project yet')
        else:
            raise NotFound({'project': f'Project {request.data["project"]} does not exist'})
    except KeyError:
        raise ValidationError({'project': 'This field is required'})
    except ValueError:
        raise ValidationError({'project': 'Incorrect type. Expected pk value, received str.'})


def all_projects_by_owner_queryset(request, queryset):
    if queryset.exists():
        return queryset.filter(owner=request.user)
    else:
        raise NotFound('No project has been created yet')
