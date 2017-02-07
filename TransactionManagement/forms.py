from django import forms
from TransactionManagement.models import BankAccount, Transaction, Bills, CheckLeaf

# izi
from UserManagement.forms import random_with_N_digits
from UserManagement.models import Customer

field_errors = {
    'required': 'وارد کردن این فیلد ضروری است.',
    'invalid': 'داده وارد شده نادرست است.'
}




class WithdrawForm(forms.Form):
    bank_account_id = forms.IntegerField(min_value=0, max_value=9999999999, error_messages=field_errors)
    amount = forms.IntegerField(min_value=0, error_messages=field_errors)

    def clean_bank_account_id(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=bank_account_id)
            if bankAccount.customer.activated == False:
                raise forms.ValidationError('این حساب مسدود است!')
        except BankAccount.DoesNotExist:
            raise forms.ValidationError('حسابی با این شماره یافت نشد!')
        return bank_account_id

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        bank_account_id = self.cleaned_data.get('bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=bank_account_id)
            if amount>bankAccount.amount:
                raise forms.ValidationError('موجودی کافی نیست!')
        except:
            raise forms.ValidationError('خطایی در مقدار وجود دارد!')
        return amount

    def save(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        amount = self.cleaned_data.get('amount')

        bank_account = BankAccount.objects.get(account_id=bank_account_id)
        bank_account.amount -= amount
        bank_account.save()



class DepositToOtherForm(forms.Form):
    source_bank_account_id = forms.IntegerField(min_value=0, error_messages=field_errors)
    destination_bank_account_id = forms.IntegerField(min_value=0, error_messages=field_errors)
    amount = forms.IntegerField(min_value=0, error_messages=field_errors)

    def clean_source_bank_account_id(self):
        source_bank_account_id = self.cleaned_data.get('source_bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=source_bank_account_id)
            if bankAccount.customer.activated == False:
                raise forms.ValidationError('این حساب مسدود است!')
        except BankAccount.DoesNotExist:
            raise forms.ValidationError('حسابی با این شماره یافت نشد!')
        return source_bank_account_id

    def clean_destination_bank_account_id(self):
        destination_bank_account_id = self.cleaned_data.get('destination_bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=destination_bank_account_id)
            if bankAccount.customer.activated == False:
                raise forms.ValidationError('این حساب مسدود است!')
        except BankAccount.DoesNotExist:
            raise forms.ValidationError('حسابی با این شماره یافت نشد!')
        return destination_bank_account_id

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        source_bank_account_id = self.cleaned_data.get('source_bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=source_bank_account_id)
            if amount>bankAccount.amount:
                raise forms.ValidationError('موجودی کافی نیست!')
        except:
            raise forms.ValidationError('خطایی در مقدار وجود دارد!')
        return amount

    def save(self):
        source_bank_account_id = self.cleaned_data.get('source_bank_account_id')
        destination_bank_account_id = self.cleaned_data.get('destination_bank_account_id')
        amount = self.cleaned_data.get('amount')

        source_bank_account = BankAccount.objects.get(account_id=source_bank_account_id)
        destination_bank_account = BankAccount.objects.get(account_id=destination_bank_account_id)
        source_bank_account.amount -= amount
        source_bank_account.save()
        destination_bank_account.amount += amount
        destination_bank_account.save()


class DepositForm(forms.Form):
    bank_account_id = forms.IntegerField(min_value=0, error_messages=field_errors)
    amount = forms.IntegerField(min_value=0, error_messages=field_errors)

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
        amount = self.cleaned_data.get('amount')

        bank_account = BankAccount.objects.get(account_id=bank_account_id)
        bank_account.amount += amount
        bank_account.save()

class BillPaymentForm(forms.Form):
    bank_account_id = forms.IntegerField(min_value=0, error_messages=field_errors)
    bill_kind = forms.CharField(error_messages=field_errors)
    bill_id = forms.IntegerField(min_value=0, error_messages=field_errors)
    amount = forms.IntegerField(min_value=0, error_messages=field_errors)

    def clean_bank_account_id(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=bank_account_id)
            if bankAccount.customer.activated == False:
                raise forms.ValidationError('این حساب مسدود است!')
        except BankAccount.DoesNotExist:
            raise forms.ValidationError('حسابی با این شماره یافت نشد!')
        return bank_account_id

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        bank_account_id = self.cleaned_data.get('bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=bank_account_id)
            if amount>bankAccount.amount:
                raise forms.ValidationError('موجودی کافی نیست!')
        except:
            raise forms.ValidationError('خطایی در مقدار وجود دارد!')
        return amount

    def save(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        bill_kind = self.cleaned_data.get('bill_kind')
        bill_id = self.cleaned_data.get('bill_id')
        amount = self.cleaned_data.get('amount')

        bank_account = BankAccount.objects.get(account_id=bank_account_id)
        bank_account.amount -= amount
        bill = Bills.objects.get(kind=bill_kind)
        bill_account = bill.BankAccount_to
        bill_account.amount += amount
        bill_account.save()
        bank_account.save()
        # BillPayment.objects.create(billpayment_id=bill_id,
        #                            billkind=bill)
                                   # bankaccount_from=bank_account)

class CashBillPaymentForm(forms.Form):
    bill_kind = forms.CharField(error_messages=field_errors)
    bill_id = forms.IntegerField(min_value=0, error_messages=field_errors)
    amount = forms.IntegerField(min_value=0, error_messages=field_errors)

    def save(self):
        bill_kind = self.cleaned_data.get('bill_kind')
        bill_id = self.cleaned_data.get('bill_id')
        amount = self.cleaned_data.get('amount')

        bill = Bills.objects.get(kind=bill_kind)
        bill_account = bill.BankAccount_to
        bill_account.amount += amount
        bill_account.save()
        # BillPayment.objects.create(billpayment_id=bill_id,
        #                            billkind=bill)


class CheckLeafRequestForm(forms.Form):
    checkleaf_id = forms.IntegerField(min_value=10000000, max_value=99999999, error_messages=field_errors)
    amount = forms.IntegerField(min_value=0, error_messages=field_errors)
    customer_to = forms.IntegerField(min_value=0, error_messages=field_errors)
    bank_account_id = forms.IntegerField(min_value=0, error_messages=field_errors)

    def clean_customer_to(self):
        customer_id = self.cleaned_data.get('customer_to')
        try:
            customer=Customer.objects.get(user__username=customer_id)
            if customer.activated == False:
                raise forms.ValidationError('این حساب کاربری مسدود است!')
        except Customer.DoesNotExist:
            raise forms.ValidationError('کاربری با این شماره یافت نشد!')
        return customer_id

    def clean_bank_account_id(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=bank_account_id)
            if bankAccount.customer.activated == False:
                raise forms.ValidationError('این حساب مسدود است!')
        except BankAccount.DoesNotExist:
            raise forms.ValidationError('حسابی با این شماره یافت نشد!')
        return bank_account_id

    def clean_checkleaf_id(self):
        checkleaf_id = self.cleaned_data.get('checkleaf_id')
        try:
            checkleaf=CheckLeaf.objects.get(checkleaf_id=checkleaf_id)
            if checkleaf.used == True:
                raise forms.ValidationError('این چک قبلا استفاده شده است!')
        except CheckLeaf.DoesNotExist:
            raise forms.ValidationError('چکی با این شماره یافت نشد!')
        return checkleaf_id



    def save(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        checkleaf_id = self.cleaned_data.get('checkleaf_id')
        amount = self.cleaned_data.get('amount')
        checkleaf = CheckLeaf.objects.get(checkleaf_id=checkleaf_id)
        customer_id = self.cleaned_data.get('customer_to')
        customer = Customer.objects.get(user__username=customer_id)
        bank_account = BankAccount.objects.get(account_id=bank_account_id)

        checkleaf.bankaccount_to=bank_account
        checkleaf.amount = amount
        checkleaf.used = True
        checkleaf.customer_to = customer
        checkleaf.save()

class CashCheckLeafRequestForm(forms.Form):
    checkleaf_id = forms.IntegerField(min_value=10000000, max_value=99999999, error_messages=field_errors)
    amount = forms.IntegerField(min_value=0, error_messages=field_errors)
    customer_to = forms.IntegerField(min_value=0, error_messages=field_errors)

    def clean_customer_to(self):
        customer_id = self.cleaned_data.get('customer_to')
        try:
            customer=Customer.objects.get(user__username=customer_id)
        except Customer.DoesNotExist:
            raise forms.ValidationError('کاربری با این شماره یافت نشد!')
        return customer_id

    def clean_checkleaf_id(self):
        checkleaf_id = self.cleaned_data.get('checkleaf_id')
        try:
            checkleaf=CheckLeaf.objects.get(checkleaf_id=checkleaf_id)
            if checkleaf.used == True:
                raise forms.ValidationError('این چک قبلا استفاده شده است!')
        except CheckLeaf.DoesNotExist:
            raise forms.ValidationError('چکی با این شماره یافت نشد!')
        return checkleaf_id



    def save(self):
        checkleaf_id = self.cleaned_data.get('checkleaf_id')
        amount = self.cleaned_data.get('amount')
        checkleaf = CheckLeaf.objects.get(checkleaf_id=checkleaf_id)
        customer_id = self.cleaned_data.get('customer_to')
        customer = Customer.objects.get(user__username=customer_id)

        checkleaf.amount = amount
        checkleaf.used = True
        checkleaf.customer_to = customer
        checkleaf.save()


# end_izi

class AccountantReportForm(forms.Form):
    national_id = forms.IntegerField(error_messages=field_errors)
    start_date = forms.DateField(error_messages=field_errors)
    end_date = forms.DateField(error_messages=field_errors)


class AdminReportForm(forms.Form):
    branch_id = forms.IntegerField(error_messages=field_errors)
    start_date = forms.DateField(required=False, error_messages=field_errors)
    end_date = forms.DateField(required=False, error_messages=field_errors)
    number_of_transaction_to = forms.IntegerField(error_messages=field_errors)
    number_of_transaction_from = forms.IntegerField(error_messages=field_errors)
