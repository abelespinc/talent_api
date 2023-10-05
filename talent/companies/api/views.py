from talent.companies.api.serializers import CompanyProfileSerializer
from talent.companies.api.serializers import CompanySerializer
from talent.companies.api.serializers import IndustrySerializer
from talent.companies.models import Company
from talent.companies.models import CompanyProfile
from talent.companies.models import Industry
from talent.core.api.views import ModelViewSet


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params

        if name := query_params.get("name"):
            queryset = queryset.filter(name__icontains=name)

        return queryset


class CompanyProfileViewSet(ModelViewSet):
    serializer_class = CompanyProfileSerializer
    queryset = CompanyProfile.objects.all()


class IndustryViewSet(ModelViewSet):
    serializer_class = IndustrySerializer
    queryset = Industry.objects.all()
