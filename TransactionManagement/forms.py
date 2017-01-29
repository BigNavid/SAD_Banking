from django import forms
from TransactionManagement.models import BankAccount

# izi

field_errors = {
    'required': 'وارد کردن این فیلد ضروری است.',
    'invalid': 'داده وارد شده نادرست است.'
}


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

    def save(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        amount = self.cleaned_data.get('amount')

        while True:
            try:
                bank_account = BankAccount.objects.get(account_id=bank_account_id)
                bank_account.amount -= amount
                bank_account.save()
                self.cleaned_data['bank_account'] = bank_account
                self.cleaned_data['amount'] = amount
                break
            except:
                pass


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

    def save(self):
        source_bank_account_id = self.cleaned_data.get('source_bank_account_id')
        destination_bank_account_id = self.cleaned_data.get('destination_bank_account_id')
        amount = self.cleaned_data.get('amount')
        while True:
            try:
                source_bank_account = BankAccount.objects.get(account_id=source_bank_account_id)
                destination_bank_account = BankAccount.objects.get(account_id=destination_bank_account_id)
                source_bank_account.amount -= amount
                source_bank_account.save()
                destination_bank_account.amount += amount
                destination_bank_account.save()
                self.cleaned_data['source_bank_account'] = source_bank_account
                self.cleaned_data['destination_bank_account'] = destination_bank_account
                self.cleaned_data['amount'] = amount
                break
            except:
                pass

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

    def save(self):
        bank_account_id = self.cleaned_data.get('bank_account_id')
        amount = self.cleaned_data.get('amount')

        while True:
            try:
                bank_account = BankAccount.objects.get(account_id=bank_account_id)
                bank_account.amount += amount
                bank_account.save()
                self.cleaned_data['bank_account'] = bank_account
                self.cleaned_data['amount'] = amount
                break
            except:
                pass

# end_izi
