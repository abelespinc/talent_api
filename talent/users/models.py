import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4, editable=False)
    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def __str__(self):
        return self.name

    def exists(self):
        return not self._state.adding and self.pk
