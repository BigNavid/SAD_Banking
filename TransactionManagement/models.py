from django.db import models

from UserManagement.models import Customer, Admin, AdminBranch, Accountant, AdminATM, Cashier, LegalExpert


class BankAccount(models.Model):
    account_id = models.BigIntegerField(primary_key=True, unique=True, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.BigIntegerField()


class Branch(models.Model):
    branch_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    admin = models.OneToOneField(AdminBranch, null=False)


class Loan(models.Model):
    loan_id = models.BigIntegerField(primary_key=True, unique=True, db_index=True)
    amount = models.BigIntegerField()
    customer = models.ForeignKey(Customer, on_delete=None)
    date_time = models.DateTimeField(auto_now=True)


class LoanPayment(models.Model):
    loanpayment_id = models.BigIntegerField(primary_key=True, unique=True, db_index=True)
    loadn = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    customer = models.ForeignKey(Customer, on_delete=None)
    date = models.DateField(db_index=True)
    paid = models.BooleanField(default=False)

class Money(models.Model):
    payment_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField()


class Bills(models.Model):
    bill_id = models.BigIntegerField(primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    BankAccount_to = models.ForeignKey(BankAccount, on_delete=models.CASCADE)


class BillPayment(models.Model):
    billpayment_id = models.BigIntegerField(primary_key=True, unique=True, db_index=True)
    billkinde = models.ForeignKey(Bills, on_delete=None)
    customer = models.ForeignKey(Customer, on_delete=None)
    bankaccount = models.ForeignKey(BankAccount, on_delete=None)


class Transaction(models.Model):
    transaction_id = models.BigIntegerField(primary_key=True, unique=True, db_index=True)
    bankaccount_from = models.ForeignKey(BankAccount, on_delete=None, related_name='From')
    bankaccount_to = models.ForeignKey(BankAccount, on_delete=None, related_name='To')
    date_time = models.DateTimeField(auto_now=True)
    amount = models.BigIntegerField()


class ATM(models.Model):
    atm_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    manager = models.ForeignKey(AdminATM, on_delete=models.CASCADE)
    amount = models.BigIntegerField()


class ATMMoneys(models.Model):
    atm_moneys_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    atm = models.ForeignKey(ATM, on_delete=models.CASCADE)
    money = models.ForeignKey(Money, on_delete=models.CASCADE)


class Czech(models.Model):
    czech_id = models.BigIntegerField(primary_key=True, unique=True, db_index=True)
    bankaccount = models.ForeignKey(BankAccount, on_delete=models.CASCADE)


class CzechLeaf(models.Model):
    czechleaf_id = models.BigIntegerField(primary_key=True, unique=True, db_index=True)
    bankaccount = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name= 'BankAccount')
    czech_id = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name= 'CzechID')
    expiration_date = models.DateField()
