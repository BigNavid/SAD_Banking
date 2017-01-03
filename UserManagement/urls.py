




from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^profile/(?P<id>[0-9]+)/', view=views.profile_customer, name='ProfileCustomer'),
    url(r'^login/', view=views.login_user, name='Login'),
    url(r'^signupCustomer/', view=views.signup_customer, name='SignUpCustomer'),
    url(r'^test/(.+)/', view=views.test, name='TestView'),
    url(r'^logout/', view=views.logout, name='Logout'),
]