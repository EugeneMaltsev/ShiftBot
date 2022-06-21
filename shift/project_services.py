from rest_framework.exceptions import ValidationError, NotFound
from shift.models import Shift, Project
import numpy as np
import pandas as pd


def shift_create(validated_data):
    shift = Shift()
    shift.user_project = validated_data['user_project']
    shift.shift_start_time = validated_data['shift_start_time']
    shift.shift_end_time = validated_data['shift_end_time']
    duration = calculate_shift_duration_time(shift)
    salary = calculate_salary_per_shift(shift)
    return Shift.objects.create(user_project_id=validated_data['user_project_id'],
                                shift_start_time=validated_data['shift_start_time'],
                                shift_end_time=validated_data['shift_end_time'],
                                shift_duration_time=duration,
                                salary_per_shift=salary)


def calculate_shift_duration_time(shift):
    shift.shift_duration_time = shift.shift_end_time - shift.shift_start_time
    shift.user_project.project_duration += shift.shift_duration_time
    shift.user_project.save()
    return shift.shift_duration_time


def calculate_salary_per_shift(shift):
    shift.salary_per_shift = (shift.shift_duration_time.seconds / 3600) * shift.user_project.salary_per_hour
    shift.user_project.project_cost += shift.salary_per_shift
    shift.user_project.save()
    return shift.salary_per_shift


def get_projects_statistics(queryset):
    df = pd.DataFrame(list(queryset.values()))
    number_of_projects = df['id'].count()
    project_cost_summary = df['project_cost'].sum()
    project_cost_mean = df['project_cost'].mean()
    project_duration_summary = df['project_duration'].sum() / np.timedelta64(1, 'h')
    project_duration_mean = df['project_duration'].mean() / np.timedelta64(1, 'h')
    statistics = ({
        'number_of_projects': number_of_projects,
        'project_cost_summary': project_cost_summary,
        'project_cost_mean': project_cost_mean,
        'project_duration_summary': project_duration_summary,
        'project_duration_mean': project_duration_mean
    })
    return statistics


def get_shift_statistics(queryset):
    df = pd.DataFrame(list(queryset.values()))
    number_of_shifts = df['id'].count()
    number_of_hours = df['shift_duration_time'].sum() / np.timedelta64(1, 'h')
    duration_mean = df['shift_duration_time'].mean() / np.timedelta64(1, 'h')
    salary_mean = df['salary_per_shift'].mean()
    statistics = ({
        'number_of_shifts': number_of_shifts,
        'number_of_hours': number_of_hours,
        'duration_mean': duration_mean,
        'salary_mean': salary_mean,
        'project_cost': queryset.first().user_project.project_cost,
    })
    return statistics


def all_shifts_by_project_queryset(request, queryset):
    try:
        if Project.objects.filter(user=request.user).filter(id=request.data['user_project']).exists():
            if queryset.filter(user_project_id=request.data['user_project']).exists():
                return queryset.filter(user_project_id=request.data['user_project'])
            else:
                raise NotFound('There are no shifts in this project yet')
        else:
            raise NotFound({'user_project': f'Project {request.data["user_project"]} does not exist'})
    except KeyError:
        raise ValidationError({'user_project': 'This field is required'})
    except ValueError:
        raise ValidationError({'user_project': 'Incorrect type. Expected pk value, received str.'})


def all_projects_by_user_queryset(request, queryset):
    if queryset.exists():
        return queryset.filter(user=request.user)
    else:
        raise NotFound('No project has been created yet')
