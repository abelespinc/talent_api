from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class OfferStatus(TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    NOT_ACTIVE = "NOT_ACTIVE", _("Not active")
    NO_STATUS = "NO_STATUS", _("No status")
    HTTP_ERROR = "HTTP_ERROR", _("HTTP Error")
    XPATH_ERROR = "XPATH_ERROR", _("XPATH Error")

    __empty__ = _("(Null)")
