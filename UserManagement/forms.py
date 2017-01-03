from .models import Customer

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

import random


class SignUpCustomerForm(forms.Form):
    field_errors = {
        'required': 'وارد کردن این فیلد ضروری است.',
        'invalid': 'داده وارد شده نادرست است.'
    }
    first_name = forms.CharField(max_length=100, error_messages=field_errors)
    last_name = forms.CharField(max_length=100, error_messages=field_errors)
    national_id = forms.IntegerField(max_value=9999999999,min_value=0)
    email = forms.EmailField(max_length=100, error_messages=field_errors)
    password = forms.CharField(widget=forms.PasswordInput, error_messages=field_errors)

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        try:
            Customer.objects.all().get(national_id=national_id)
            raise forms.ValidationError('این شماره ملی قبلا ثبت شده است.')
        except Customer.DoesNotExist:
            return national_id

    def save(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        national_id = self.cleaned_data.get('national_id')

        while (True):
            try:
                number = random.randint(1000000, 9999999)
                user = User.objects.create_user(username=number, password=password, email=email, first_name=first_name,
                                                last_name=last_name)
                user.save()
                self.cleaned_data['user'] = user
                break
            except:
                pass

        customer = Customer()
        customer.user = user
        customer.national_id = national_id

        customer.save()
        group = Group.objects.get(name='Customer')
        group.user_set.add(user)
