from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from talent.core.models import Model
from talent.jobs.services.locations import get_location_standard_locations


class Job(Model):
    name = models.TextField(_("Name"), unique=True)
    slug = models.SlugField(_("Name slug"), max_length=128, blank=True)

    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")
        ordering = ("name",)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)


class Temporality(Model):
    name = models.TextField(_("Name"), unique=True)

    class Meta:
        verbose_name = _("Temporality")
        verbose_name_plural = _("Temporalities")
        ordering = ("name",)


class Attendance(Model):
    name = models.TextField(_("Name"), unique=True)

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")
        ordering = ("name",)


class ContractType(Model):
    name = models.TextField(_("Name"), unique=True)

    class Meta:
        verbose_name = _("Contract type")
        verbose_name_plural = _("Contract types")
        ordering = ("name",)


class ExperienceLevel(Model):
    name = models.TextField(_("Name"), unique=True)
    years = models.IntegerField(_("Years"), unique=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Experience level")
        verbose_name_plural = _("Experience levels")
        ordering = ("name",)


class EducationLevel(Model):
    name = models.TextField(_("Name"), unique=True)

    class Meta:
        verbose_name = _("Education level")
        verbose_name_plural = _("Education levels")
        ordering = ("name",)


class Skill(Model):
    name = models.TextField(_("Name"), unique=True)

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ("name",)


class Location(Model):
    name = models.TextField(_("Name"), unique=True)
    slug = models.SlugField(_("Name slug"), max_length=128, blank=True)
    subregion = models.ForeignKey(
        "cities_light.SubRegion",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("SubRegion (Province)"),
    )
    city = models.ForeignKey(
        "cities_light.City",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("City"),
    )

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ("name",)
        indexes = [models.Index(fields=["name"])]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        if not self.has_standard_location:
            self.city, self.subregion = get_location_standard_locations(location=self)

        return super().save(*args, **kwargs)

    @property
    def has_standard_location(self):
        return bool(self.subregion or self.city)
