from django import forms
from django.contrib.auth.models import User

from TransactionManagement import Constants
from TransactionManagement.Utils import random_with_N_digits
from .models import Customer, Admin, AdminBranch, BranchStaff, Cashier, Accountant, LegalExpert, AdminATM
from TransactionManagement.models import BankAccount, Branch, CreditCard, Bills, Check, CheckLeaf, Loan, Bank,\
    RegularTransfers

field_errors = {
    'required': 'وارد کردن این فیلد ضروری است.',
    'invalid': 'داده وارد شده نادرست است.'
}


class CreateBankAccountForm(forms.Form):
    customer_username = forms.IntegerField(max_value=99999, min_value=10000, error_messages=field_errors)
    amount = forms.IntegerField(min_value=10000, error_messages=field_errors)

    def clean_customer_to(self):
        customer_id = self.cleaned_data.get('customer_to')
        try:
            customer=Customer.objects.get(user__username=customer_id)
        except Customer.DoesNotExist:
            raise forms.ValidationError('کاربری با این شماره یافت نشد!')
        return customer_id

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
    bank_account_id = forms.IntegerField(min_value=0, error_messages=field_errors)
    password = forms.IntegerField(max_value=9999, min_value=1000, error_messages=field_errors)

    def clean_bank_account_id(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=bank_account_id)
            if bankAccount.customer.activated == False:
                raise forms.ValidationError('این حساب مسدود است!')
        except BankAccount.DoesNotExist:
            raise forms.ValidationError('حسابی با این شماره یافت نشد!')
        return bank_account_id

    def save(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        bank_account = BankAccount.objects.get(account_id=bank_account_id)
        password = self.cleaned_data.get('password')

        while True:
            try:
                creditcard_id = random_with_N_digits(10)
                credit_card = CreditCard.objects.create(number=creditcard_id,
                                                        bank_account=bank_account,
                                                        password=password)
                self.cleaned_data['credit_card'] = credit_card
                break
            except:
                pass


class LoanRequestForm(forms.Form):
    bank_account_id = forms.IntegerField(min_value=0, error_messages=field_errors)
    amount = forms.IntegerField(min_value=0, error_messages=field_errors)
    installments = forms.IntegerField(min_value=0, error_messages=field_errors)

    def clean_bank_account_id(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=bank_account_id)
            if bankAccount.customer.activated == False:
                raise forms.ValidationError('این حساب مسدود است!')
        except BankAccount.DoesNotExist:
            raise forms.ValidationError('حسابی با این شماره یافت نشد!')
        return bank_account_id

    def save(self,cashier):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        bank_account = BankAccount.objects.get(account_id=bank_account_id)
        amount = self.cleaned_data.get('amount')
        installments = self.cleaned_data.get('installments')

        while True:
            try:
                Loan_id = random_with_N_digits(5)
                loan = Loan.objects.create(loan_id=Loan_id,
                                           bank_account=bank_account,
                                           amount=amount,
                                           installments=installments,
                                           customer=bank_account.customer,
                                           cashier=cashier)
                # self.cleaned_data['Loan'] = loan
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
        customer = Customer.objects.get(user__username=Constants.BILL_USER_ACCOUNT)
        branch = Branch.objects.get(branch_id=Constants.MAIN_BRANCH)
        bank_account = BankAccount.objects.create(account_id=bank_account_id,
                                                  customer=customer,
                                                  amount=0,
                                                  branch=branch)
        Bills.objects.create(BankAccount_to=bank_account, kind=kind)



class CheckRequestForm(forms.Form):
    bank_account_id = forms.IntegerField(min_value=1000000000, max_value=9999999999, error_messages=field_errors)

    def clean_bank_account_id(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=bank_account_id)
            if bankAccount.customer.activated == False:
                raise forms.ValidationError('این حساب مسدود است!')
            return bank_account_id
        except BankAccount.DoesNotExist:
            raise forms.ValidationError('حسابی با این شماره یافت نشد!')

    def save(self):
        while True:
            try:
                check_id = random_with_N_digits(6)
                bank_account_id = self.cleaned_data.get('bank_account_id')
                bank_account=BankAccount.objects.get(account_id=bank_account_id)
                check = Check.objects.create(check_id=check_id,
                                             bankaccount=bank_account)
                checkLeaf_id= random_with_N_digits(8)
                checkLeaf_list = []
                for i in range(checkLeaf_id,checkLeaf_id+10):
                    checkLeaf= CheckLeaf.objects.create(checkleaf_id=i,
                                                        bankaccount_from=bank_account,
                                                        parent_check=check,
                                                        amount=0)
                    checkLeaf_list.append(checkLeaf)
                return checkLeaf_list
            except:
                pass

class LegalExpertCheckConfirmForm(forms.Form):
    checkleaf_id = forms.IntegerField(min_value=10000000, max_value=99999999, error_messages=field_errors)

class AccountantCheckConfirmForm(forms.Form):
    checkleaf_id = forms.IntegerField(min_value=10000000, max_value=99999999, error_messages=field_errors)

class ActivateAccountForm(forms.Form):
    customer_username = forms.IntegerField(max_value=99999, min_value=10000, error_messages=field_errors)

class LoanConfirmationForm(forms.Form):
    loan_id = forms.IntegerField(min_value=10000, max_value=99999, error_messages=field_errors)


class FeeForm(forms.Form):
    profit = forms.IntegerField(min_value=0, error_messages=field_errors)
    card_fee = forms.IntegerField(min_value=0, error_messages=field_errors)
    check_fee = forms.IntegerField(min_value=0, error_messages=field_errors)
    alert_fee = forms.IntegerField(min_value=0, error_messages=field_errors)
    card_transfer_fee = forms.IntegerField(min_value=0, error_messages=field_errors)
    bankaccount_transfer_fee = forms.IntegerField(min_value=0, error_messages=field_errors)

    def save(self):
        bank = Bank.objects.get(name="FaBank")
        bank.profit = self.cleaned_data.get('profit')
        bank.card_fee = self.cleaned_data.get('card_fee')
        bank.check_fee = self.cleaned_data.get('check_fee')
        bank.alert_fee = self.cleaned_data.get('alert_fee')
        bank.card_transfer_fee = self.cleaned_data.get('card_transfer_fee')
        bank.bankaccount_transfer_fee = self.cleaned_data.get('bankaccount_transfer_fee')
        bank.save()


class RegularTransactionForm(forms.Form):
    type = forms.CharField(max_length=10)
    bankaccount_from = forms.IntegerField(error_messages=field_errors)
    bankaccount_to = forms.IntegerField(error_messages=field_errors)
    amount = forms.IntegerField(min_value=0, error_messages=field_errors)

    def save(self):
        type = self.cleaned_data.get('type')
        bankaccount_from = self.cleaned_data.get('bankaccount_from')
        bankaccount_to = self.cleaned_data.get('bankaccount_to')
        amount = self.cleaned_data.get('amount')
        try:
            while True:
                regular_transaction_id = random_with_N_digits(5)
                regular_transaction = None
                if type == 'Daily':
                    regular_transaction = RegularTransfers.objects.create(regular_trasaction_id=regular_transaction_id,
                                                                          isDaily=True, bankaccount_from=
                                                                          bankaccount_from, bankaccount_to=
                                                                          bankaccount_to, amount=amount)
                elif type == 'Monthly':
                    regular_transaction = RegularTransfers.objects.create(regular_trasaction_id=regular_transaction_id,
                                                                          isMonthly=True, bankaccount_from=
                                                                          bankaccount_from, bankaccount_to=
                                                                          bankaccount_to, amount=amount)
                elif type == 'Yearly':
                    regular_transaction = RegularTransfers.objects.create(regular_trasaction_id=regular_transaction_id,
                                                                          isYearly=True, bankaccount_from=
                                                                          bankaccount_from, bankaccount_to=
                                                                          bankaccount_to, amount=amount)
                self.cleaned_data['regular_transaction'] = regular_transaction
                break
        except:
            pass
