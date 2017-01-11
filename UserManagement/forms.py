import random

from django import forms
from django.contrib.auth.models import User

from .models import Customer, Admin, AdminBranch, BranchStaff
from TransactionManagement.models import BankAccount, Branch


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


field_errors = {
    'required': 'وارد کردن این فیلد ضروری است.',
    'invalid': 'داده وارد شده نادرست است.'
}


class CreateBankAccountForm(forms.Form):
    customer_username = forms.IntegerField(max_value=99999, min_value=10000, error_messages=field_errors)
    amount = forms.IntegerField(min_value=0, error_messages=field_errors)

    def save(self):
        customer_username = self.cleaned_data.get('customer_username')
        amount = self.cleaned_data.get('amount')

        while True:
            try:
                bank_account_id = random_with_N_digits(10)
                customer = Customer.objects.get(user__username=customer_username)
                bank_account = BankAccount.objects.create(account_id=bank_account_id, customer=customer, amount=amount)
                bank_account.save()
                self.cleaned_data['bank_account'] = bank_account
                break
            except:
                pass


class CreateBranchForm(forms.Form):
    name = forms.CharField(max_length=255, error_messages=field_errors)
    address = forms.CharField(max_length=10000, error_messages=field_errors)

    def save(self):
        name = self.cleaned_data.get('name')
        address = self.cleaned_data.get('address')

        while True:
            try:
                branch_id = random_with_N_digits(4)
                print(branch_id)
                branch = Branch.objects.create(branch_id=branch_id, name=name, address=address)
                branch.save()
                self.cleaned_data['branch'] = branch
                break
            except:
                pass


class SignUpBranchAdminForm(forms.Form):
    first_name = forms.CharField(max_length=255, error_messages=field_errors)
    last_name = forms.CharField(max_length=255, error_messages=field_errors)
    branch = forms.IntegerField(max_value=9999, min_value=1000, error_messages=field_errors)
    national_id = forms.IntegerField(error_messages=field_errors)
    email = forms.EmailField(max_length=255, error_messages=field_errors)
    password = forms.CharField(widget=forms.PasswordInput, error_messages=field_errors)

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        try:
            Admin.objects.get(national_id=national_id)
            raise forms.ValidationError('این شماره ملی قبلا ثبت شده است.')
        except Admin.DoesNotExist:
            return national_id

    def clean_branch(self):
        branch = self.cleaned_data.get('branch')
        try:
            Branch.objects.get(branch_id=branch)
            return branch
        except Branch.DoesNotExist:
            raise forms.ValidationError('این شماره شعبه معتبر نمی‌باشد.')

    def save(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        national_id = self.cleaned_data.get('national_id')
        branch = self.cleaned_data.get('branch')

        while True:
            try:
                branch_admin_id = random_with_N_digits(5)
                user = User.objects.create_user(username=branch_admin_id, password=password, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                self.cleaned_data['user'] = user
                break
            except:
                pass

        branch_staff = BranchStaff()
        branch_staff.user = user
        branch_staff.national_id = national_id
        branch_staff.branch = Branch.objects.get(branch_id=branch)
        branch_staff.save()

        branch_admin = AdminBranch()
        branch_admin.user = branch_staff
        branch_admin.save()



class SignUpAdminForm(forms.Form):
    first_name = forms.CharField(max_length=255, error_messages=field_errors)
    last_name = forms.CharField(max_length=255, error_messages=field_errors)
    national_id = forms.IntegerField(error_messages=field_errors)
    email = forms.EmailField(max_length=255, error_messages=field_errors)
    phone = forms.IntegerField(error_messages=field_errors)
    password = forms.CharField(widget=forms.PasswordInput, error_messages=field_errors)

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        try:
            Admin.objects.get(national_id=national_id)
            raise forms.ValidationError('این شماره ملی قبلا ثبت شده است.')
        except Admin.DoesNotExist:
            return national_id

    def save(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        national_id = self.cleaned_data.get('national_id')
        phone = self.cleaned_data.get('phone')

        while True:
            try:
                admin_id = random_with_N_digits(5)
                user = User.objects.create_user(username=admin_id, password=password, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                self.cleaned_data['user'] = user
                break
            except:
                pass

        admin = Admin()
        admin.user = user
        admin.national_id = national_id
        admin.phone = phone

        admin.save()


class SignUpCustomerForm(forms.Form):
    first_name = forms.CharField(max_length=255, error_messages=field_errors)
    last_name = forms.CharField(max_length=255, error_messages=field_errors)
    national_id = forms.IntegerField(error_messages=field_errors)
    email = forms.EmailField(max_length=255, error_messages=field_errors)
    phone = forms.IntegerField(error_messages=field_errors)
    password = forms.CharField(widget=forms.PasswordInput, error_messages=field_errors)
    notification = forms.BooleanField(required=False)

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
                customer_id = random_with_N_digits(5)
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
