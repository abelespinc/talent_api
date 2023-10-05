from rest_framework import serializers

from talent.core.api.serializers import ModelSerializer
from talent.jobs.models import Attendance
from talent.jobs.models import ContractType
from talent.jobs.models import EducationLevel
from talent.jobs.models import ExperienceLevel
from talent.jobs.models import Job
from talent.jobs.models import Location
from talent.jobs.models import Skill
from talent.jobs.models import Temporality


class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = ["id", "name"]


class TemporalitySerializer(ModelSerializer):
    class Meta:
        model = Temporality
        fields = ["id", "name"]


class AttendanceSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "name"]


class ContractTypeSerializer(ModelSerializer):
    class Meta:
        model = ContractType
        fields = ["id", "name"]


class ExperienceLevelSerializer(ModelSerializer):
    class Meta:
        model = ExperienceLevel
        fields = ["id", "name", "years"]


class EducationLevelSerializer(ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = ["id", "name"]


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name"]


class LocationForSearchSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ["id"]


class SalarySerializer(serializers.Serializer):
    min = serializers.IntegerField(required=False, allow_null=True)
    max = serializers.IntegerField(required=False, allow_null=True)
