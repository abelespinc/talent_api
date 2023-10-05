from django.apps import AppConfig
from django.db.utils import ProgrammingError
from django.utils.translation import gettext_lazy as _


def create_config_object():
    # Create the Config singleton
    from talent.core.models import Configuration

    try:
        if not Configuration.objects.exists():
            Configuration.objects.create()
    except ProgrammingError:
        pass


class CoreConfig(AppConfig):
    name = "talent.core"
    verbose_name = _("Core")

    def ready(self):
        create_config_object()
