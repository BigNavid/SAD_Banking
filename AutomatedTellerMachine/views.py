from django.shortcuts import render

from TransactionManagement.models import CreditCard
from TransactionManagement.Utils import CreateTansactionModel
from TransactionManagement.Constants import WITHDRAW_ATM, DEPOSIT_TO_OTHER_ACCOUNT_ATM, DEPOSIT_TO_OTHER_CREDITCARD_ATM


def atm_login(request):
    msg = ''
    if request.method == 'POST':
        cardnumber = request.POST['cardNumber']
        print("cardNumber: ", cardnumber)
        password = request.POST['password']
        print("password: ", password)
        amount = request.POST['amount']
        amount = int(amount)
        print("amount: ", amount)
        is_withdraw_cash = request.POST['is_withdraw_cash']
        is_deposit_to_credit_card = request.POST['is_deposit_to_credit_card']
        is_deposit_to_bank_account = request.POST['is_deposit_to_bank_account']
        to_credit_card = request.POST['to_credit_card']
        to_bank_account = request.POST['to_bank_account']


        try:
            print("Finding CreditCard...")
            creditcard = CreditCard.objects.get(number=cardnumber, password=password)
            print("Card Found")
            if creditcard.bank_account.customer.activated:
                print("CustomerAccount Activated")
                if is_withdraw_cash:
                    bankaccount_from = creditcard.bank_account
                    print("BankAccount.Amount: ", bankaccount_from.amount)
                    if bankaccount_from.amount >= amount:
                        print("BankAccount.Amount greater than amount")
                        bankaccount_from.amount -= amount
                        print("NEW BankAccount.Amount: ", bankaccount_from.amount)
                        bankaccount_from.save()
                        print("Saved")
                        CreateTansactionModel(bankaccount_from=bankaccount_from,
                                              branch_from=bankaccount_from.branch,
                                              amount=amount,
                                              type=WITHDRAW_ATM)
                        print("Transaction Created")
                        msg = 'از کارت شما به شماره کارت {} مبلغ {} برداشته شد.'.format(creditcard.number, amount)
                    else:
                        msg = 'موجودی کارت کافی نمی‌باشد.'
                elif is_deposit_to_credit_card:
                    pass
                elif is_deposit_to_bank_account:
                    pass
            else:
                msg = 'حساب کاربری شما غیر فعال می‌باشد.'
        except:
            msg = 'شماره کارت/رمز عبور اشتباه است.'

    context = {'msg': msg}
    return render(request, 'atm_index.html', context)
