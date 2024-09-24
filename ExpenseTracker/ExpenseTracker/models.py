from django.db import models # type: ignore
from django.utils.timezone import now # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.conf import settings # type: ignore
from django.db.models.signals import post_save # type: ignore
from django.dispatch import receiver # type: ignore
from django.db.models import Sum # type: ignore

#Create your models here

SELECT_CATEGORY_CHOICE = [
    ("Food", "Food"),
    ("Shopping", "Shopping"),
    ("Necessities","Necessities"),
    ("")
]