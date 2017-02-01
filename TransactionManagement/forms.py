from django import forms
from TransactionManagement.models import BankAccount, Transaction

# izi
from UserManagement.forms import random_with_N_digits

field_errors = {
    'required': 'وارد کردن این فیلد ضروری است.',
    'invalid': 'داده وارد شده نادرست است.'
}

CASH_DEPOSIT = "cash_deposit"
DEPOSIT_TO_OTHER_ACCOUNT = "deposit_to_other_account"
CASH_WITHDRAW = "cash_withdraw"



class WithdrawForm(forms.Form):
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

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        bank_account_id = self.cleaned_data.get('bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=bank_account_id)
            if amount>bankAccount.amount:
                raise forms.ValidationError('موجودی کافی نیست!')
        except:
            raise forms.ValidationError('خطایی در مقدار وجود دارد!')

    def save(self,cashier):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        amount = self.cleaned_data.get('amount')

        bank_account = BankAccount.objects.get(account_id=bank_account_id)
        bank_account.amount -= amount
        bank_account.save()

        while True:
            try:
                transaction_id = random_with_N_digits(6)
                transaction = Transaction(transaction_id=transaction_id)
                break
            except:
                pass

        transaction.bankaccount_from = bank_account_id
        transaction.amount = amount
        transaction.cashier = cashier
        transaction.branch = cashier.user.branch
        transaction.type = CASH_WITHDRAW
        transaction.save()





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

    def clean_destination_bank_account_id(self):
        destination_bank_account_id = self.cleaned_data.get('destination_bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=destination_bank_account_id)
            if bankAccount.customer.activated == False:
                raise forms.ValidationError('این حساب مسدود است!')
        except BankAccount.DoesNotExist:
            raise forms.ValidationError('حسابی با این شماره یافت نشد!')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        source_bank_account_id = self.cleaned_data.get('source_bank_account_id')
        try:
            bankAccount=BankAccount.objects.get(account_id=source_bank_account_id)
            if amount>bankAccount.amount:
                raise forms.ValidationError('موجودی کافی نیست!')
        except:
            raise forms.ValidationError('خطایی در مقدار وجود دارد!')

    def save(self,cashier):
        source_bank_account_id = self.cleaned_data.get('source_bank_account_id')
        destination_bank_account_id = self.cleaned_data.get('destination_bank_account_id')
        amount = self.cleaned_data.get('amount')

        source_bank_account = BankAccount.objects.get(account_id=source_bank_account_id)
        destination_bank_account = BankAccount.objects.get(account_id=destination_bank_account_id)
        source_bank_account.amount -= amount
        source_bank_account.save()
        destination_bank_account.amount += amount
        destination_bank_account.save()

        while True:
            try:
                transaction_id = random_with_N_digits(6)
                transaction = Transaction(transaction_id=transaction_id)
                break
            except:
                pass

        transaction.bankaccount_from = source_bank_account_id
        transaction.bankaccount_to = destination_bank_account_id
        transaction.amount = amount
        transaction.cashier = cashier
        transaction.branch = cashier.user.branch
        transaction.type = DEPOSIT_TO_OTHER_ACCOUNT
        transaction.save()

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

    def save(self,cashier):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        amount = self.cleaned_data.get('amount')

        bank_account = BankAccount.objects.get(account_id=bank_account_id)
        bank_account.amount += amount
        bank_account.save()

        while True:
            try:
                transaction_id = random_with_N_digits(6)
                transaction = Transaction(transaction_id=transaction_id)
                break
            except:
                pass

        transaction.bankaccount_to = bank_account_id
        transaction.amount = amount
        transaction.cashier = cashier
        transaction.branch = cashier.user.branch
        transaction.type = CASH_DEPOSIT
        transaction.save()

# end_izi
