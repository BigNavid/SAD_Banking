import random

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from .models import Customer


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


field_errors = {
    'required': 'وارد کردن این فیلد ضروری است.',
    'invalid': 'داده وارد شده نادرست است.'
}


class SignUpCustomerForm(forms.Form):
    first_name = forms.CharField(max_length=100, error_messages=field_errors)
    last_name = forms.CharField(max_length=100, error_messages=field_errors)
    national_id = forms.IntegerField(max_value=9999999999, min_value=0, error_messages=field_errors)
    email = forms.EmailField(max_length=100, error_messages=field_errors)
    phone = forms.IntegerField(error_messages=field_errors)
    password = forms.CharField(widget=forms.PasswordInput, error_messages=field_errors)
    notification = forms.BooleanField()

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
        phone = self.cleaned_data.get('phone')
        notification = self.cleaned_data.get('notification')

        while True:
            try:
                customer_id = random_with_N_digits(10)
                user = User.objects.create_user(username=customer_id, password=password, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                self.cleaned_data['user'] = user
                break
            except:
                pass

        customer = Customer()
        customer.user = user
        customer.national_id = national_id
        customer.phone = phone
        customer.notification = notification

        customer.save()
        group = Group.objects.get(name='Customer')
        group.user_set.add(user)
