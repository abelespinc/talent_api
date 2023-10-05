import json
from pprint import pprint

from django.core.serializers.json import DjangoJSONEncoder

from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from talent.companies.api.serializers import CompanySerializer
from talent.companies.api.serializers import CompanyWithProfileSerializer
from talent.companies.models import Company
from talent.companies.models import Industry
from talent.core.api.serializers import CreatableSlugRelatedField
from talent.core.api.serializers import ModelSerializer
from talent.jobs.api.serializers import SalarySerializer
from talent.jobs.models import Attendance
from talent.jobs.models import ContractType
from talent.jobs.models import EducationLevel
from talent.jobs.models import ExperienceLevel
from talent.jobs.models import Job
from talent.jobs.models import Location
from talent.jobs.models import Skill
from talent.jobs.models import Temporality
from talent.offers.api.serializer_examples import OFFER_AI_INFO_EXAMPLE
from talent.offers.api.serializer_examples import OFFER_WRITE_SERIALIZER_EXAMPLE
from talent.offers.models import Offer
from talent.offers.models import OfferAiInfo
from talent.offers.models import OfferDuplicate
from talent.offers.models import Recruiter
from talent.offers.models import Source
from talent.offers.services.offers import get_offer_info_field
from talent.offers.services.offers import get_offer_salary
from talent.offers.services.offers import get_offer_similarities


class OfferDetailDuplicateSerializer(ModelSerializer):
    source = serializers.CharField(source="source.name", default=None)

    class Meta:
        model = Offer
        fields = ["url", "source"]


@extend_schema_serializer(examples=[OpenApiExample("New offer", value=OFFER_WRITE_SERIALIZER_EXAMPLE)])
class OfferWriteSerializer(ModelSerializer):
    job = CreatableSlugRelatedField(slug_field="name", queryset=Job.objects.all())
    source = CreatableSlugRelatedField(slug_field="name", queryset=Source.objects.all())
    temporality = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Temporality.objects.all(),
        required=False,
        allow_null=True,
    )
    attendance = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Attendance.objects.all(),
        required=False,
        allow_null=True,
    )
    recruiter = CreatableSlugRelatedField(
        slug_field="name",
        queryset=Recruiter.objects.all(),
        required=False,
        allow_null=True,
    )
    industry = CreatableSlugRelatedField(
        slug_field="name",
        queryset=Industry.objects.all(),
        required=False,
        allow_null=True,
    )
    location = CreatableSlugRelatedField(
        slug_field="name",
        queryset=Location.objects.all(),
        required=False,
        allow_null=True,
    )
    skills = CreatableSlugRelatedField(
        slug_field="name",
        queryset=Skill.objects.all(),
        required=False,
        many=True,
    )
    contract_type = serializers.SlugRelatedField(
        slug_field="name",
        queryset=ContractType.objects.all(),
        required=False,
        allow_null=True,
    )
    education_level = CreatableSlugRelatedField(
        slug_field="name",
        queryset=EducationLevel.objects.all(),
        required=False,
        allow_null=True,
    )
    experience_level = CreatableSlugRelatedField(
        slug_field="name",
        queryset=ExperienceLevel.objects.all(),
        required=False,
        allow_null=True,
    )
    company = CompanyWithProfileSerializer(required=False, allow_null=True)
    salary = SalarySerializer(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "offer_id",  # Required
            "job",  # Required
            "url",  # Required
            "source",  # Required
            "status",
            "company",
            "temporality",
            "attendance",
            "contract_type",
            "recruiter",
            "industry",
            "location",
            "education_level",
            "experience_level",
            "skills",
            "description",  # Required
            "posting_date",  # Required
            "valid_until",
            "salary",
            "duplicates",
        ]
        extra_kwargs = {"id": {"read_only": True}, "status": {"required": False}}

    def validate(self, data):
        # Add the source field to allow company profile creation
        company = data.get("company")

        if company and "source" not in company:
            data["company"]["source"] = data["source"]

        return super().validate(data)

    def create(self, validated_data):
        """
        We must override the create method because we have nested writable serializers
        """
        company = self.fields["company"].create(validated_data.pop("company"))
        skills = validated_data.pop("skills", [])

        offer = Offer.objects.create(**validated_data, company=company)
        offer.skills.set(skills)

        return offer


class OfferReadSerializer(ModelSerializer):
    job = serializers.CharField(source="job.name", default=None)
    temporality = serializers.CharField(source="temporality.name", default=None)
    attendance = serializers.CharField(source="attendance.name", default=None)
    contract_type = serializers.CharField(source="contract_type.name", default=None)
    location = serializers.CharField(source="location.name", default=None)
    company = serializers.SerializerMethodField()
    duplicates_count = serializers.SerializerMethodField()
    salary = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "job",
            "url",
            "status",
            "company",
            "location",
            "salary",
            "temporality",
            "attendance",
            "contract_type",
            "posting_date",
            "duplicates_count",
        ]

    def get_company(self, offer: Offer):
        if company := offer.company:
            return {"name": company.name, "is_competitor": company.is_competitor}
        return None

    def get_duplicates_count(self, offer: Offer):
        return offer.duplicates.count()

    def get_salary(self, offer: Offer):
        return get_offer_salary(offer=offer)


class OfferDetailReadSerializer(ModelSerializer):
    job = serializers.CharField(source="job.name", default=None)
    temporality = serializers.SerializerMethodField()
    attendance = serializers.SerializerMethodField()
    contract_type = serializers.SerializerMethodField()
    company = CompanySerializer()
    source = serializers.CharField(source="source.name", default=None)
    recruiter = serializers.CharField(source="recruiter.name", default=None)
    industry = serializers.CharField(source="industry.name", default=None)
    location = serializers.SerializerMethodField()
    education_level = serializers.CharField(source="education_level.name", default=None)
    experience_level = serializers.CharField(source="experience_level.name", default=None)
    skills = serializers.SerializerMethodField()
    duplicates = OfferDetailDuplicateSerializer(many=True)
    similarities = serializers.SerializerMethodField()
    salary = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "offer_id",
            "job",
            "url",
            "source",
            "status",
            "company",
            "temporality",
            "attendance",
            "contract_type",
            "recruiter",
            "industry",
            "location",
            "education_level",
            "experience_level",
            "skills",
            "description",
            "posting_date",
            "valid_until",
            "salary",
            "duplicates",
            "similarities",
        ]

    def get_similarities(self, offer: Offer):
        return get_offer_similarities(offer=offer)

    def get_skills(self, offer: Offer):
        skills = get_offer_info_field(offer=offer, field="skills")
        return [skill.name for skill in skills.all()] if skills else []

    def get_temporality(self, offer: Offer):
        temporality = get_offer_info_field(offer=offer, field="temporality")
        return temporality and temporality.name

    def get_attendance(self, offer: Offer):
        attendance = get_offer_info_field(offer=offer, field="attendance")
        return attendance and attendance.name

    def get_contract_type(self, offer: Offer):
        contract_type = get_offer_info_field(offer=offer, field="contract_type")
        return contract_type and contract_type.name

    def get_location(self, offer: Offer):
        location = get_offer_info_field(offer=offer, field="location")
        return location and {"name": location.name, "has_standard_location": location.has_standard_location}

    def get_salary(self, offer: Offer):
        return get_offer_info_field(offer=offer, field="salary")


@extend_schema_serializer(examples=[OpenApiExample("New offer AI info", value=OFFER_AI_INFO_EXAMPLE)])
class OfferAiInfoSerializer(ModelSerializer):
    temporality = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Temporality.objects.all(),
        required=False,
        allow_null=True,
    )
    attendance = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Attendance.objects.all(),
        required=False,
        allow_null=True,
    )
    location = CreatableSlugRelatedField(
        slug_field="name",
        queryset=Location.objects.all(),
        required=False,
        allow_null=True,
    )
    skills = CreatableSlugRelatedField(
        slug_field="name",
        queryset=Skill.objects.all(),
        required=False,
        many=True,
    )
    contract_type = serializers.SlugRelatedField(
        slug_field="name",
        queryset=ContractType.objects.all(),
        required=False,
        allow_null=True,
    )
    salary = SalarySerializer(required=False, allow_null=True)

    class Meta:
        model = OfferAiInfo
        fields = [
            "id",
            "offer",
            "job_title",
            "description",
            "basic_taxonomy",
            "advanced_taxonomy",
            "salary",
            "location",
            "temporality",
            "attendance",
            "contract_type",
            "skills",
        ]


class OfferDuplicateSerializer(ModelSerializer):
    class Meta:
        model = OfferDuplicate
        fields = [
            "id",
            "from_offer",
            "to_offer",
            "job_title_similarity",
            "description_similarity",
            "contract_type_similarity",
            "temporality_similarity",
            "location_similarity",
            "attendance_similarity",
        ]


class SourceSerializer(ModelSerializer):
    class Meta:
        model = Source
        fields = ["id", "name"]


class RecruiterSerializer(ModelSerializer):
    class Meta:
        model = Recruiter
        fields = ["id", "name", "url"]
