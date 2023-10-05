from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models import F
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from talent.core.models import Model
from talent.offers.model_utils import get_default_salary_json
from talent.offers.utils import OfferStatus


class OfferWithEmptyFieldsCountManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                empty_fields_count=(
                    models.Case(
                        models.When(models.Q(temporality__isnull=True), then=1),
                        default=0,
                    )
                    + models.Case(
                        models.When(models.Q(attendance__isnull=True), then=1),
                        default=0,
                    )
                    + models.Case(
                        models.When(models.Q(contract_type__isnull=True), then=1),
                        default=0,
                    )
                    + models.Case(
                        models.When(models.Q(education_level__isnull=True), then=1),
                        default=0,
                    )
                    + models.Case(
                        models.When(models.Q(experience_level__isnull=True), then=1),
                        default=0,
                    )
                )
            )
        )


class Offer(Model):
    offer_id = models.TextField(_("Offer ID"), unique=True)
    url = models.URLField(_("URL"), max_length=2048)
    status = models.TextField(
        _("Status"),
        choices=OfferStatus.choices,
        blank=True,
        default=OfferStatus.ACTIVE,
    )
    job = models.ForeignKey(
        "jobs.Job",
        on_delete=models.SET_NULL,
        related_name="offers",
        null=True,
        verbose_name=_("Job title"),
    )
    source = models.ForeignKey(
        "offers.Source",
        on_delete=models.SET_NULL,
        related_name="offers",
        null=True,
        verbose_name=_("Source"),
    )
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.SET_NULL,
        related_name="offers",
        null=True,
        verbose_name=_("Company"),
    )
    temporality = models.ForeignKey(
        "jobs.Temporality",
        on_delete=models.SET_NULL,
        related_name="offers",
        null=True,
        verbose_name=_("Temporality"),
    )
    attendance = models.ForeignKey(
        "jobs.Attendance",
        on_delete=models.SET_NULL,
        related_name="offers",
        null=True,
        verbose_name=_("Attendance"),
    )
    contract_type = models.ForeignKey(
        "jobs.ContractType",
        on_delete=models.SET_NULL,
        related_name="offers",
        null=True,
        verbose_name=_("Contract type"),
    )
    recruiter = models.ForeignKey(
        "offers.Recruiter",
        on_delete=models.SET_NULL,
        related_name="offers",
        blank=True,
        null=True,
        verbose_name=_("Recruiter"),
    )
    industry = models.ForeignKey(
        "companies.Industry",
        related_name="offers",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Industry"),
    )
    location = models.ForeignKey(
        "jobs.Location",
        related_name="offers",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Location"),
    )
    education_level = models.ForeignKey(
        "jobs.EducationLevel",
        related_name="offers",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Education level"),
    )
    experience_level = models.ForeignKey(
        "jobs.ExperienceLevel",
        related_name="offers",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Experience"),
    )
    skills = models.ManyToManyField(
        "jobs.Skill",
        related_name="offers",
        blank=True,
        verbose_name=_("Skills"),
    )
    duplicates = models.ManyToManyField(
        "self",
        through="offers.OfferDuplicate",
        blank=True,
        verbose_name=_("Duplicates"),
    )
    description = models.TextField(_("Description"), blank=True, null=True)
    description_search_vector = SearchVectorField(blank=True, null=True)
    posting_date = models.DateTimeField(_("Posting date"), blank=True, null=True)
    valid_until = models.DateTimeField(_("Valid until"), blank=True, null=True)
    salary = models.JSONField(_("Salary"), blank=True, null=True, default=get_default_salary_json)

    objects = models.Manager()
    objects_with_empty_fields_count = OfferWithEmptyFieldsCountManager()

    class Meta:
        verbose_name = _("Offer")
        verbose_name_plural = _("Offers")
        ordering = ("company__sort_order", "-posting_date")
        indexes = [GinIndex(fields=["description_search_vector"])]

    def __str__(self):
        return f"{self.source} - {self.job}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.update_search_vector()

    def update_search_vector(self):
        Offer.objects.filter(pk=self.pk).update(description_search_vector=SearchVector("description"))


class OfferAiInfo(Model):
    """
    This model stores data that has been extracted from the original offer using AI
    """

    offer = models.OneToOneField(
        "offers.Offer",
        on_delete=models.CASCADE,
        related_name="ai_info",
        verbose_name=_("Offer"),
    )
    job_title = models.TextField(_("Job title (translated)"))
    job_title_slug = models.SlugField(_("Job title slug"), max_length=256, blank=True)
    description = models.TextField(_("Description (translated)"), blank=True, null=True)
    basic_taxonomy = models.TextField(_("Basic taxonomy"), blank=True, null=True)
    advanced_taxonomy = models.TextField(_("Advanced taxonomy"), blank=True, null=True)
    salary = models.JSONField(_("Salary (AI)"), blank=True, null=True, default=get_default_salary_json)
    location = models.ForeignKey(
        "jobs.Location",
        related_name="offers_ai",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Location (AI)"),
    )
    temporality = models.ForeignKey(
        "jobs.Temporality",
        on_delete=models.SET_NULL,
        related_name="offers_ai",
        null=True,
        verbose_name=_("Temporality (AI)"),
    )
    attendance = models.ForeignKey(
        "jobs.Attendance",
        on_delete=models.SET_NULL,
        related_name="offers_ai",
        null=True,
        verbose_name=_("Attendance (AI)"),
    )
    contract_type = models.ForeignKey(
        "jobs.ContractType",
        on_delete=models.SET_NULL,
        related_name="offers_ai",
        null=True,
        verbose_name=_("Contract type (AI)"),
    )
    skills = models.ManyToManyField(
        "jobs.Skill",
        related_name="offers_ai",
        blank=True,
        verbose_name=_("Skills (AI)"),
    )

    class Meta:
        verbose_name = _("Offer AI info")
        verbose_name_plural = _("Offers AI info")

    def save(self, *args, **kwargs):
        self.job_title_slug = slugify(self.job_title)

        return super().save(*args, **kwargs)


class OfferDuplicate(Model):
    from_offer = models.ForeignKey(
        "offers.Offer",
        on_delete=models.CASCADE,
        related_name="duplicates_from",
        verbose_name=_("From offer"),
    )
    to_offer = models.ForeignKey(
        "offers.Offer",
        on_delete=models.CASCADE,
        related_name="duplicates_to",
        verbose_name=_("To offer"),
    )
    job_title_similarity = models.SmallIntegerField(_("Job title similarity (1-100)"), blank=True, null=True)
    description_similarity = models.SmallIntegerField(_("Description similarity (1-100)"), blank=True, null=True)
    contract_type_similarity = models.SmallIntegerField(_("Contract type similarity (1-100)"), blank=True, null=True)
    temporality_similarity = models.SmallIntegerField(_("Temporality similarity (1-100)"), blank=True, null=True)
    location_similarity = models.SmallIntegerField(_("Location similarity (1-100)"), blank=True, null=True)
    attendance_similarity = models.SmallIntegerField(_("Attendance similarity (1-100)"), blank=True, null=True)

    class Meta:
        verbose_name = _("Offer duplicate")
        verbose_name_plural = _("Offer duplicates")


class Source(Model):
    name = models.TextField(_("Name"), unique=True)

    class Meta:
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")
        ordering = ("name",)


class Recruiter(Model):
    name = models.TextField(_("Name"))
    url = models.URLField(_("URL"), max_length=2048, blank=True, null=True)

    class Meta:
        verbose_name = _("Recruiter")
        verbose_name_plural = _("Recruiters")
        ordering = ("name",)
