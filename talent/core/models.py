import uuid

from django.contrib.postgres.fields import ArrayField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import gettext_lazy as _


class Model(models.Model):
    """
    Base Model. It's meant to replace Django's models.Model

    We want all primary keys to be UUID
    We want an extra_data field that can store a JSON with whatever information is needed
    We want fields to keep track of object creation and edition details
    """

    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(_("Is active?"), blank=True, default=True)
    extra_data = models.JSONField(_("Extra data"), blank=True, default=dict, encoder=DjangoJSONEncoder)
    created_at = models.DateTimeField(_("Creation date"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last modification date"), auto_now=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="created_%(class)ss",
        blank=True,
        null=True,
        verbose_name=_("Created by"),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return getattr(self, "name", super().__str__())

    def exists(self):
        return not self._state.adding and self.pk


class Configuration(models.Model):
    status_scrapy_enabled = models.BooleanField(
        _("Status scrapy enabled"),
        blank=True,
        default=False,
        help_text=_("Is the scrapy enabled?"),
    )
    status_scrapy_periodicity = models.SmallIntegerField(
        _("Status scrapy periodicity"),
        blank=True,
        default=2,
        help_text=_("Active offers will be checked every X days"),
    )
    status_scrapy_days_to_start = models.SmallIntegerField(
        _("Status scrapy days to start"),
        blank=True,
        default=4,
        help_text=_("Active offers will be checked X days after they are saved"),
    )
    status_scrapy_duration = models.SmallIntegerField(
        _("Status scrapy duration"),
        blank=True,
        default=7 * 2,
        help_text=_("Active offers will be checked for X days"),
    )
    scrapy_job_keywords = ArrayField(models.TextField(), blank=True, default=list)

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configuration")

    def __str__(self):
        return str(_("Configuration"))

    def save(self, *args, **kwargs):
        """
        Only one Config object can exist
        """
        if type(self).objects.exists() and not self.exists():
            return None
        return super().save(*args, **kwargs)

    def exists(self):
        return not self._state.adding and self.pk
