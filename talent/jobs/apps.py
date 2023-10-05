from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class JobsConfig(AppConfig):
    name = "talent.jobs"
    verbose_name = _("Jobs")
