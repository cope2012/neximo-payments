import logging

from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from model_utils.models import TimeStampedModel

logger = logging.getLogger(__name__)


def _default_providers():
    return {}


class User(AbstractUser, TimeStampedModel):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "password"]

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100, null=False)

    username = None
    first_name = None
    last_name = None
    last_login = None
    date_joined = None

