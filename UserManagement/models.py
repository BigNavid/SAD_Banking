from django.contrib.auth.models import User
from django.db import models

# from TransactionManagement.models import Branch


class Admin(models.Model):
    user = models.OneToOneField(User)


class AdminBranch(models.Model):
    user = models.OneToOneField(User)
    # branch = models.OneToOneField(Branch, unique=True, null=True, blank=True)


class Accountant(models.Model):
    user = models.OneToOneField(User)


class Cashier(models.Model):
    user = models.OneToOneField(User)


class LegalExpert(models.Model):
    user = models.OneToOneField(User)


class AdminATM(models.Model):
    user = models.OneToOneField(User)


class Customer(models.Model):
    user = models.OneToOneField(User)
    national_id = models.IntegerField(unique=True)
    phone = models.IntegerField(unique=False, null=True, blank=True)
    notification = models.BooleanField(unique=False, null=False)
