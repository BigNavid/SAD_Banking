from django import forms
from django.contrib.auth.models import User

from TransactionManagement.Utils import random_with_N_digits
from .models import Customer, Admin, AdminBranch, BranchStaff, Cashier, Accountant, LegalExpert, AdminATM
from TransactionManagement.models import BankAccount, Branch, CreditCard, Bills

field_errors = {
    'required': 'وارد کردن این فیلد ضروری است.',
    'invalid': 'داده وارد شده نادرست است.'
}


class CreateBankAccountForm(forms.Form):
    customer_username = forms.IntegerField(max_value=99999, min_value=10000, error_messages=field_errors)
    amount = forms.IntegerField(min_value=0, error_messages=field_errors)

    def save(self,branch):
        customer_username = self.cleaned_data.get('customer_username')
        amount = self.cleaned_data.get('amount')

        customer = Customer.objects.get(user__username=customer_username)
        while True:
            try:
                bank_account_id = random_with_N_digits(10)
                bank_account = BankAccount.objects.create(account_id=bank_account_id,
                                                          customer=customer,
                                                          amount=amount,
                                                          branch=branch)
                bank_account.save()
                self.cleaned_data['bank_account'] = bank_account
                break
            except:
                pass


class CreateCreditCardForm(forms.Form):
    bank_account_id = forms.IntegerField(error_messages=field_errors)

    def save(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')

        while True:
            try:
                creditcard_id = random_with_N_digits(10)
                credit_card = CreditCard.objects.create(number=creditcard_id,
                                                        bank_account_id=bank_account_id)
                self.cleaned_data['credit_card'] = credit_card
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


class SignUpStaffForm(forms.Form):
    first_name = forms.CharField(max_length=255, error_messages=field_errors)
    last_name = forms.CharField(max_length=255, error_messages=field_errors)
    post = forms.CharField(max_length=255, error_messages=field_errors)
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

    # def clean_branch(self):
    #     branch = self.cleaned_data.get('branch')
    #     try:
    #         Branch.objects.get(branch_id=branch)
    #         return branch
    #     except Branch.DoesNotExist:
    #         raise forms.ValidationError('این شماره شعبه معتبر نمی‌باشد.')

    def save(self,Branch):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        national_id = self.cleaned_data.get('national_id')
        branch = Branch
        post= self.cleaned_data.get('post')

        while True:
            try:
                branch_staff_id = random_with_N_digits(5)
                user = User.objects.create_user(username=branch_staff_id, password=password, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                self.cleaned_data['user'] = user
                break
            except:
                pass

        branch_staff = BranchStaff()
        branch_staff.user = user
        branch_staff.national_id = national_id
        branch_staff.branch = branch
        branch_staff.save()
        if post=="Cashier":
            employee = Cashier()
        elif post=="Accountant":
            employee = Accountant()
        elif post=="LegalExpert":
            employee = LegalExpert()
        elif post=="AdminATM":
            employee = AdminATM()
        employee.user = branch_staff
        employee.save()


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

class BillDefinitionForm(forms.Form):
    kind = forms.CharField(max_length=255, error_messages=field_errors)
    bank_account_id = forms.IntegerField(min_value=1000000000, max_value=9999999999, error_messages=field_errors)

    def clean_bank_account_id(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=bank_account_id)
            raise forms.ValidationError('شماره حساب وارد شده تکراری است!')
        except BankAccount.DoesNotExist:
            return bank_account_id

    def save(self):
        kind = self.cleaned_data.get('kind')
        bank_account_id = self.cleaned_data.get('bank_account_id')
        customer = Customer.objects.get(user__username=13222)
        branch = Branch.objects.get(branch_id=2782)
        bank_account = BankAccount.objects.create(account_id=bank_account_id,
                                                  customer=customer,
                                                  amount=0,
                                                  branch=branch)
        Bills.objects.create(BankAccount_to=bank_account, kind=kind)
