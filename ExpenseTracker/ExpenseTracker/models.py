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
    ("Entertainment", "Entertainment"),
    ("Other", "Other")
]

ADD_EXPENSE_CHOICE = [
    ("Expense", "Expense"),
    ("Income", "Income")
]

PROFESSION_CHOICES = [
    ("Employee", "Employee"),
    ("Business", "Business"),
    ("Student", "Student"),
    ("Other", "Other")
]

class Addmoney_info(models.Model):
    user = models.ForeginKey(User,default = 1, on_delete=models.CASCADE)
    add_money = models.CharField(max_lenght = 10, choices = ADD_EXPENSE_CHOICE)
    quantity = models.BigIntergerField()
    Date = models.DataField(default = now)
    Category = models.CharField(max_length = 20, choices = SELECT_CATEGORY_CHOICES, default = 'Food')

    class Meta:
        db.table: 'addmoney'


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    profession = models.CharField(max_length = 10, choices = PROFESSION_CHOICES)
    Savings = models.IntegerField (null=True, blank=True)
    income = models.BigIntegerField (null = True, blank =True)
    image = models.ImageField(upload_to = 'profile_image', blank=True)
    def__str__(self):
    return self.user.username
    