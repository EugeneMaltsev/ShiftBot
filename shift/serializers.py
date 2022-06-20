from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shift import project_services
from shift.models import Project, Shift, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Project
        fields = '__all__'


class ShiftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shift
        fields = '__all__'

    def validate(self, attrs):
        if attrs['shift_start_time'] > attrs['shift_end_time']:
            raise ValidationError({'shift_end_time': 'shift_end_time must occur after shift_start_time'})
        return attrs

    def create(self, validated_data):
        return project_services.shift_create(validated_data)


class ProjectStatisticSerializer(serializers.ModelSerializer):
    number_of_projects = serializers.IntegerField()
    project_cost_summary = serializers.FloatField()
    project_cost_mean = serializers.FloatField()
    project_duration_summary = serializers.FloatField()
    project_duration_mean = serializers.FloatField()

    class Meta:
        model = Shift
        fields = ['number_of_projects',
                  'project_cost_summary',
                  'project_cost_mean',
                  'project_duration_summary',
                  'project_duration_mean']


class ShiftStatisticSerializer(serializers.ModelSerializer):
    number_of_shifts = serializers.IntegerField()
    number_of_hours = serializers.FloatField()
    duration_mean = serializers.FloatField()
    salary_mean = serializers.FloatField()
    project_cost = serializers.FloatField()

    class Meta:
        model = Shift
        fields = ['number_of_shifts',
                  'number_of_hours',
                  'duration_mean',
                  'salary_mean',
                  'project_cost']
