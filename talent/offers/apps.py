from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OffersConfig(AppConfig):
    name = "talent.offers"
    verbose_name = _("Offers")
