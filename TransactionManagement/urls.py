from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^withdrawBankAccount/', view=views.withdraw_from_bank_account, name='WithdrawBankAccount'),
    url(r'^DepositBankAccount/', view=views.deposit_to_bank_account, name='DepositBankAccount'),
    url(r'^DepositToOtherBankAccount/', view=views.deposit_to_other_bank_account, name='DepositToOtherBankAccount'),
    url(r'^aReport/', view=views.accountant_report, name='AccountantReport')
]
