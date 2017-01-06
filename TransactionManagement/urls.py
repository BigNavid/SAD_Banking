from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^atm/', view=views.atm_login, name='ATMLogin'),
    url(r'^whithdrawBankAccount/', view=views.whithdraw_from_bank_account, name='WhithdrawBankAccount'),
]
