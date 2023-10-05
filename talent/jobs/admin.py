from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from talent.core.admin import ModelAdmin
from talent.jobs.models import Attendance
from talent.jobs.models import ContractType
from talent.jobs.models import EducationLevel
from talent.jobs.models import ExperienceLevel
from talent.jobs.models import Job
from talent.jobs.models import Location
from talent.jobs.models import Skill
from talent.jobs.models import Temporality


@admin.register(Job)
class JobAdmin(ModelAdmin):
    fieldsets = ((None, {"fields": ("name",)}),)
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Temporality)
class TemporalityAdmin(ModelAdmin):
    fieldsets = ((None, {"fields": ("name",)}),)
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Attendance)
class AttendanceAdmin(ModelAdmin):
    fieldsets = ((None, {"fields": ("name",)}),)
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ContractType)
class ContractTypeAdmin(ModelAdmin):
    fieldsets = ((None, {"fields": ("name",)}),)
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ExperienceLevel)
class ExperienceLevelAdmin(ModelAdmin):
    fieldsets = ((None, {"fields": (("name", "years"),)}),)
    list_display = ("name", "years")
    search_fields = ("name", "years")


@admin.register(EducationLevel)
class EducationLevelAdmin(ModelAdmin):
    fieldsets = ((None, {"fields": ("name",)}),)
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    fieldsets = ((None, {"fields": ("name",)}),)
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(ModelAdmin):
    fieldsets = (
        (None, {"fields": ("name",)}),
        (_("Standard locations"), {"fields": (("city", "subregion"),)}),
    )
    list_display = ("name", "city", "subregion")
    search_fields = ("name",)
