from django.contrib.auth.models import User
from django.db import models


class Admin(models.Model):
    user = models.OneToOneField(User)
    profit = models.IntegerField(default=18)


class Branch(models.Model):
    branch_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)


class BranchStaff(models.Model):
    user = models.OneToOneField(User)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    national_id = models.IntegerField(unique=True)


class AdminBranch(models.Model):
    user = models.OneToOneField(BranchStaff)


class Accountant(models.Model):
    user = models.OneToOneField(BranchStaff)


class Cashier(models.Model):
    user = models.OneToOneField(BranchStaff)


class LegalExpert(models.Model):
    user = models.OneToOneField(BranchStaff)


class AdminATM(models.Model):
    user = models.OneToOneField(BranchStaff)


class Customer(models.Model):
    user = models.OneToOneField(User)
    national_id = models.IntegerField(unique=True)
    phone = models.IntegerField(unique=False, null=True, blank=True)
    notification = models.BooleanField(default=False, null=False)
    activated = models.BooleanField(default=False, null=False)
