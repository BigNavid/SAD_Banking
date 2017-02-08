from django import forms

from TransactionManagement.models import ATM, Branch
from UserManagement.models import AdminATM



class CreateATMForm(forms.Form):
    manager_id = forms.IntegerField(min_value=0)
    amount = forms.IntegerField(min_value=0)

