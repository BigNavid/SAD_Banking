from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^atm/', view=views.atm, name='ATM'),
    url(r'^whithdrawBankAccount/', view=views.whithdraw_from_bank_account, name='WhithdrawBankAccount'),
]
