from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^atm/', view=views.atm_login, name='ATMLogin'),
]
