from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Temporalities(TextChoices):
    FULL_TIME = "FULL_TIME", _("Full time")
    FULL_TIME_DEFAULT = "FULL_TIME_DEFAULT", _("Full time (default)")
    PART_TIME = "PART_TIME", _("Part time")

    __empty__ = _("(Null)")


class Attendances(TextChoices):
    ON_SITE = "ON_SITE", _("On site")
    ON_SITE_DEFAULT = "ON_SITE_DEFAULT", _("On site (default)")
    REMOTE = "REMOTE", _("Remote")
    PARTIALLY_REMOTE = "PARTIALLY_REMOTE", _("Partially remote")

    __empty__ = _("(Null)")


class ContractTypes(TextChoices):
    FIXED = "FIXED", _("Fixed")
    FIXED_DEFAULT = "FIXED_DEFAULT", _("Fixed (default)")
    TEMPORAL = "TEMPORAL", _("Temporal")
    INTERNSHIP = "INTERNSHIP", _("Internship")
    CONTRACTOR = "CONTRACTOR", _("Contractor")
    FREELANCE = "FREELANCE", _("Freelance")
    OTHERS = "OTHERS", _("Others")

    __empty__ = _("(Null)")


class LocationTypes(TextChoices):
    CITY = "CITY", _("City")
    SUBREGION = "SUBREGION", _("Subregion")

    __empty__ = _("(Null)")
