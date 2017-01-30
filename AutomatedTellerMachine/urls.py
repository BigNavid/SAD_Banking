from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^', view=views.atm_login, name='ATMLogin'),
    url(r'^services/', view=views.choose_service, name='Services'),
]
