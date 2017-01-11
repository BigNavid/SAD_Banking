from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', view=views.login_user, name='Login'),
    url(r'^superUser/signupAdmin/', view=views.signup_admin, name='SignUpAdmin'),
    url(r'^admin/createBranch/', view=views.create_branch, name='CreateBranch'),
    url(r'^cashier/signupCustomer/', view=views.signup_customer, name='SignUpCustomer'),
    url(r'^cashier/createBankAccount/', view=views.create_bank_account, name='CreateBankAccount'),
    url(r'^profile/cashier/(.+)/', view=views.profile_cashier, name='ProfileCashier'),
    url(r'^profile/customer/(.+)/', view=views.profile_customer, name='ProfileCustomer'),
    url(r'^test/(.+)/', view=views.test, name='TestView'),
    url(r'^logout/', view=views.logout_view, name='Logout'),
]