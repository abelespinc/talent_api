from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from talent.core.api.views import ModelViewSet
from talent.jobs.api.serializers import AttendanceSerializer
from talent.jobs.api.serializers import ContractTypeSerializer
from talent.jobs.api.serializers import EducationLevelSerializer
from talent.jobs.api.serializers import ExperienceLevelSerializer
from talent.jobs.api.serializers import JobSerializer
from talent.jobs.api.serializers import LocationSerializer
from talent.jobs.api.serializers import SkillSerializer
from talent.jobs.api.serializers import TemporalitySerializer
from talent.jobs.models import Attendance
from talent.jobs.models import ContractType
from talent.jobs.models import EducationLevel
from talent.jobs.models import ExperienceLevel
from talent.jobs.models import Job
from talent.jobs.models import Location
from talent.jobs.models import Skill
from talent.jobs.models import Temporality
from talent.jobs.services.locations import get_locations_for_search


class JobViewSet(ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.all()


class TemporalityViewSet(ModelViewSet):
    serializer_class = TemporalitySerializer
    queryset = Temporality.objects.all()


class AttendanceViewSet(ModelViewSet):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()


class ContractTypeViewSet(ModelViewSet):
    serializer_class = ContractTypeSerializer
    queryset = ContractType.objects.all()


class ExperienceLevelViewSet(ModelViewSet):
    serializer_class = ExperienceLevelSerializer
    queryset = ExperienceLevel.objects.all()


class EducationLevelViewSet(ModelViewSet):
    serializer_class = EducationLevelSerializer
    queryset = EducationLevel.objects.all()


class SkillViewSet(ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    @action(methods=["GET"], detail=False)
    def search(self, request):
        search_text = request.query_params.get("name")

        if not search_text:
            raise ValidationError("Name is required")

        return Response(get_locations_for_search(search_text=search_text))
