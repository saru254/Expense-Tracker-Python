from django.db import models # type: ignore
from django.utils.timezone import now # type: ignore
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
