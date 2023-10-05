from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from talent.core.models import Configuration


class ModelAdmin(admin.ModelAdmin):
    def get_fieldsets(self, request, obj=None):
        return (
            *super().get_fieldsets(request, obj),
            (_("Meta"), {"fields": ("is_active", "created_by", ("created_at", "updated_at"), "id")}),
        )

    def get_readonly_fields(self, request, obj=None):
        return (*super().get_readonly_fields(request, obj), "id", "created_at", "updated_at")

    def get_ordering(self, request):
        return (*super().get_ordering(request), "-updated_at")

    def get_autocomplete_fields(self, request):
        return (*super().get_autocomplete_fields(request), "created_by")

    def get_search_fields(self, request):
        return (*super().get_search_fields(request), "pk")


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("Scraping"),
            {
                "fields": (
                    "status_scrapy_enabled",
                    "status_scrapy_periodicity",
                    "status_scrapy_days_to_start",
                    "status_scrapy_duration",
                    "scrapy_job_keywords",
                )
            },
        ),
    )
