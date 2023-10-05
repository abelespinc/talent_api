from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from talent.core.models import Model


class Company(Model):
    name = models.TextField(_("Name"), unique=True)
    slug = models.SlugField(_("Name slug"), max_length=256, blank=True)
    is_competitor = models.BooleanField(_("Is competitor?"), blank=True, default=False)
    sort_order = models.PositiveSmallIntegerField(_("Sort order"), unique=True, blank=True, null=True)
    industry = models.ForeignKey(
        "companies.Industry",
        related_name="companies",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Industry"),
    )

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ("name",)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)


class CompanyProfile(Model):
    company = models.ForeignKey(
        "companies.Company",
        related_name="profiles",
        on_delete=models.CASCADE,
        verbose_name=_("Company"),
    )
    source = models.ForeignKey(
        "offers.Source",
        related_name="company_profiles",
        on_delete=models.CASCADE,
        verbose_name=_("Source"),
    )
    url = models.URLField(_("URL"), blank=True, null=True)

    class Meta:
        verbose_name = _("Company profile")
        verbose_name_plural = _("Company profiles")

    @property
    def company_name(self):
        return str(self.company)

    @property
    def source_name(self):
        return str(self.source)


class Industry(Model):
    name = models.TextField(_("Name"), unique=True)

    class Meta:
        verbose_name = _("Industry")
        verbose_name_plural = _("Industries")
        ordering = ("name",)
