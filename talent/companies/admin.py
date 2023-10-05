from django.contrib import admin

from talent.companies.models import Company
from talent.companies.models import CompanyProfile
from talent.companies.models import Industry
from talent.core.admin import ModelAdmin


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    fieldsets = ((None, {"fields": (("name", "is_competitor"), "sort_order")}),)
    list_display = ("name", "is_competitor")
    list_filter = ("is_competitor",)
    search_fields = ("name",)


@admin.register(CompanyProfile)
class CompanyProfileAdmin(ModelAdmin):
    fieldsets = ((None, {"fields": (("company", "source"), "url")}),)
    list_display = ("company_name", "source_name", "url")
    list_filter = ("company__is_competitor", "source")
    search_fields = ("company__name", "source__name")
    autocomplete_fields = ("company", "source")


@admin.register(Industry)
class IndustryAdmin(ModelAdmin):
    fieldsets = ((None, {"fields": ("name",)}),)
    list_display = ("name",)
    search_fields = ("name",)
