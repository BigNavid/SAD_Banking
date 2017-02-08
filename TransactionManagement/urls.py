from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^withdrawBankAccount/', view=views.withdraw_from_bank_account, name='WithdrawBankAccount'),
    url(r'^DepositBankAccount/', view=views.deposit_to_bank_account, name='DepositBankAccount'),
    url(r'^DepositToOtherBankAccount/', view=views.deposit_to_other_bank_account, name='DepositToOtherBankAccount'),
    url(r'^AccountantReport/', view=views.accountant_report, name='AccountantReport'),
    url(r'^AdminReport/', view=views.admin_report, name='AdminReport'),
    url(r'^CustomerReport/', view=views.customer_report, name='CustomerReport'),
    url(r'^BillPayment/', view=views.bill_payment, name='BillPayment'),
    url(r'^CashBillPayment/', view=views.cash_bill_payment, name='CashBillPayment'),
    url(r'^CheckLeafRequest/', view=views.checkleaf_request, name='CheckLeafRequest'),
    url(r'^CashCheckLeafRequest/', view=views.cash_checkleaf_request, name='CashCheckLeafRequest'),
    url(r'^MoneyDeclaration/', view=views.money_declaration, name='MoneyDeclaration'),
    url(r'^MoneyEdit/', view=views.money_edit, name='MoneyEdit'),

]
