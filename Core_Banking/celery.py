from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from django.conf import settings
import datetime

import django
django.setup()

from TransactionManagement.models import BankAccount, Bank, LoanPayment
from UserManagement.notification import loan_payment_not_paid_notif, loan_payment_paid_notif

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core_Banking.settings')
app = Celery('Core_Banking')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@periodic_task(run_every=(crontab(minute='*/1')), name="some_task", ignore_result=True)
def some_task():
    print("Hi testing Celery every minutes")


@periodic_task(run_every=(crontab(0, 0, day_of_month='1')), name="profit", ignore_result=True)
def profit():
    bank_accounts = BankAccount.objects.all()
    for bank_account in bank_accounts:
        bank_account.amount += bank_account.profit_until_now
        bank_account.profit_until_now = 0
        bank_account.save()


@periodic_task(run_every=(crontab(minute=0, hour=0)), name="profit_calculate", ignore_result=True)
def profit_calculate():
    bank_accounts = BankAccount.objects.all()
    bank = Bank.objects.all()[0]
    for bank_account in bank_accounts:
        profit_today = int(bank_account.amount * (bank.profit/365))
        bank_account.profit_until_now += profit_today
        bank_account.save()


@periodic_task(run_every=(crontab(minute=0, hour=0)), name="loan_payment", ignore_result=True)
def loan_payment():
    today = datetime.date.today()
    loan_payments = LoanPayment.objects.all().filter(paid=False, date=today)
    for payment in loan_payments:
        bank_account = payment.loan.bank_account
        if bank_account.amount >= payment.amount:
            bank_account.amount -= payment.amount
            bank_account.save()
            payment.paid = True
            payment.save()
            loan_payment_paid_notif(payment.loanpayment_id)
        else:
            bank_account.customer.activated = False
            bank_account.customer.save()
            loan_payment_not_paid_notif(payment.loanpayment_id)


@periodic_task(run_every=(crontab(minute=0, hour=0)), name="loan_payment", ignore_result=True)
def loan_payment():
    today = datetime.date.today()
    loan_payments = LoanPayment.objects.all().filter(paid=False, date=today)
    for payment in loan_payments:
        bank_account = payment.loan.bank_account
        if bank_account.amount >= payment.amount:
            bank_account.amount -= payment.amount
            bank_account.save()
            payment.paid = True
            payment.save()
            loan_payment_paid_notif(payment.loanpayment_id)
        else:
            bank_account.customer.activated = False
            bank_account.customer.save()
            loan_payment_not_paid_notif(payment.loanpayment_id)
