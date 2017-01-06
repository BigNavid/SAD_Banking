from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profile/(?P<id>[0-9]+)/', view=views.profile_customer, name='ProfileCustomer'),
    url(r'^login/', view=views.login_user, name='Login'),
    url(r'^signupCustomer/', view=views.signup_customer, name='SignUpCustomer'),
    url(r'^createBankAccount/', view=views.create_bank_account, name='CreateBankAccount'),
    url(r'^profile/(.+)/', view=views.profile_cashier, name='ProfileCashier'),
    url(r'^test/(.+)/', view=views.test, name='TestView'),
    url(r'^logout/', view=views.logout_view, name='Logout'),
]