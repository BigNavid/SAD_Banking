from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^atm/', view=views.atm, name='ATM'),
    url(r'^withdrawBankAccount/', view=views.withdraw_from_bank_account, name='WithdrawBankAccount'),
    url(r'^DepositBankAccount/', view=views.deposit_to_bank_account, name='DepositBankAccount'),
]
