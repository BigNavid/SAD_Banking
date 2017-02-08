from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^Index/', view=views.atm_login, name='ATMLogin'),
    url(r'^Create/', view=views.create_atm, name='Create'),
]
