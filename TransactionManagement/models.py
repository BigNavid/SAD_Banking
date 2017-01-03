from django.db import models

from UserManagement.models import Customer, Admin, AdminBranch, Accountant, AdminATM, Cashier, LegalExpert


class Branch(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    address = models.TextField(blank=True, null=True)
    admin = models.OneToOneField(AdminBranch, null=False)


class Account(models.Model):
    number = models.IntegerField()
    customer = models.ForeignKey(Customer, null=True, blank=True)


class ATM(models.Model):
    atm_id = models.IntegerField('شناسه خودپرداز', primary_key=True, unique=True, db_index=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='ATMs')
    manager = models.ForeignKey(AdminATM, on_delete=models.CASCADE, related_name='ATMs')
