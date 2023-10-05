from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from talent.core.admin import ModelAdmin
from talent.offers.models import Offer
from talent.offers.models import OfferAiInfo
from talent.offers.models import OfferDuplicate
from talent.offers.models import Recruiter
from talent.offers.models import Source


@admin.register(Offer)
class OfferAdmin(ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("offer_id", "status"),
                    ("job", "salary"),
                    ("posting_date", "valid_until"),
                    ("source", "url"),
                    "description",
                )
            },
        ),
        (_("Company"), {"fields": (("company", "industry"),)}),
        (
            _("Job"),
            {
                "fields": (
                    ("contract_type", "temporality"),
                    ("location", "attendance"),
                    ("education_level", "experience_level"),
                    "skills",
                )
            },
        ),
        (_("Recruiter"), {"fields": ("recruiter",)}),
    )
    list_display = ("offer_id", "job", "status", "company", "source", "recruiter", "posting_date", "valid_until")
    list_filter = (
        "status",
        "source",
        "temporality",
        "attendance",
        "contract_type",
        "education_level",
        "experience_level",
    )
    search_fields = (
        "job__name",
        "source__name",
        "company__name",
        "recruiter__name",
        "industry__name",
        "location__name",
        "description",
    )
    autocomplete_fields = (
        "temporality",
        "attendance",
        "contract_type",
        "education_level",
        "experience_level",
        "job",
        "company",
        "recruiter",
        "industry",
        "location",
        "skills",
    )


@admin.register(OfferAiInfo)
class OfferAiInfoAdmin(ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "offer",
                    ("job_title", "salary"),
                    ("basic_taxonomy", "advanced_taxonomy"),
                    "description",
                )
            },
        ),
        (
            _("Job"),
            {
                "fields": (
                    ("contract_type", "temporality"),
                    ("location", "attendance"),
                    "skills",
                )
            },
        ),
    )
    list_display = ("offer", "job_title")
    list_filter = ("temporality", "attendance", "contract_type")
    search_fields = (
        "offer__pk",
        "offer__offer_id",
        "job_title",
        "location__name",
        "description",
    )
    autocomplete_fields = (
        "temporality",
        "attendance",
        "contract_type",
        "offer",
        "location",
        "skills",
    )


@admin.register(OfferDuplicate)
class OfferDuplicateAdmin(ModelAdmin):
    fieldsets = (
        (
            None,
            {"fields": (("from_offer", "to_offer"),)},
        ),
        (
            _("Similarity"),
            {
                "fields": (
                    ("job_title_similarity", "description_similarity"),
                    ("contract_type_similarity", "temporality_similarity"),
                    ("location_similarity", "attendance_similarity"),
                )
            },
        ),
    )
    list_display = ("pk", "from_offer", "to_offer")
    search_fields = ("pk", "from_offer__pk", "to_offer__pk")
    autocomplete_fields = ("from_offer", "to_offer")


@admin.register(Source)
class SourceAdmin(ModelAdmin):
    fieldsets = ((None, {"fields": ("name",)}),)
    list_display = ("name", "offer_count")
    search_fields = ("name",)

    def offer_count(self, source: Source):
        return source.offers.count()


@admin.register(Recruiter)
class RecruiterAdmin(ModelAdmin):
    fieldsets = ((None, {"fields": (("name", "url"),)}),)
    list_display = ("name", "url")
    search_fields = ("name",)
