from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shift import project_services
from shift.models import Project, Shift, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Project
        fields = '__all__'


class ShiftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shift
        fields = '__all__'

    def validate(self, attrs):
        if attrs['start_time'] > attrs['end_time']:
            raise ValidationError({'end_time': 'end_time must occur after start_time'})
        return attrs

    def create(self, validated_data):
        return project_services.shift_create(validated_data)


class ProjectStatisticSerializer(serializers.ModelSerializer):
    amount_of_projects = serializers.IntegerField()
    bill_summary = serializers.FloatField()
    bill_mean = serializers.FloatField()
    duration_summary = serializers.FloatField()
    duration_mean = serializers.FloatField()

    class Meta:
        model = Shift
        fields = ['amount_of_projects',
                  'bill_summary',
                  'bill_mean',
                  'duration_summary',
                  'duration_mean']


class ShiftStatisticSerializer(serializers.ModelSerializer):
    amount_of_shifts = serializers.IntegerField()
    amount_of_hours = serializers.FloatField()
    duration_mean = serializers.FloatField()
    wage_mean = serializers.FloatField()
    bill = serializers.FloatField()

    class Meta:
        model = Shift
        fields = ['amount_of_shifts',
                  'amount_of_hours',
                  'duration_mean',
                  'wage_mean',
                  'bill']
