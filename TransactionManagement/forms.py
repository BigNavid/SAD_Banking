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
