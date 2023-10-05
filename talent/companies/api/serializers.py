from rest_framework import serializers

from talent.companies.models import Company
from talent.companies.models import CompanyProfile
from talent.companies.models import Industry
from talent.core.api.serializers import CreatableSlugRelatedField
from talent.core.api.serializers import ModelSerializer
from talent.offers.models import Source


class CompanyProfileSerializer(ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ["id", "company", "source", "url"]


class CompanyProfileDetailSerializer(ModelSerializer):
    source = serializers.CharField(source="source.name", default=None)

    class Meta:
        model = CompanyProfile
        fields = ["source", "url"]


class CompanySerializer(ModelSerializer):
    offers = serializers.SerializerMethodField()
    industry = serializers.CharField(source="industry.name", default=None)
    profiles = CompanyProfileDetailSerializer(many=True)

    class Meta:
        model = Company
        fields = ["id", "name", "is_competitor", "industry", "offers", "profiles"]

    def get_offers(self, company: Company):
        return company.offers.count()


class CompanyWithProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    source = CreatableSlugRelatedField(slug_field="name", queryset=Source.objects.all(), required=False)
    url = serializers.URLField()
    is_competitor = serializers.BooleanField()

    def create(self, validated_data):
        """
        Get or create the company and the profile
        Return the company
        """
        company = Company.objects.get_or_create(
            name=validated_data["name"],
            defaults={"is_competitor": validated_data["is_competitor"]},
        )[0]
        CompanyProfile.objects.get_or_create(
            company=company,
            source=validated_data["source"],
            defaults={"url": validated_data["url"]},
        )

        return company

    def to_representation(self, instance):
        """
        Use the CompanySerializer to_representation method
        """
        return CompanySerializer(instance=instance).to_representation(instance)


class IndustrySerializer(ModelSerializer):
    class Meta:
        model = Industry
        fields = ["id", "name"]
