from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from TransactionManagement.models import CreditCard, ATM, BankAccount
from TransactionManagement.Utils import CreateTansactionModel, random_with_N_digits
from TransactionManagement.Constants import WITHDRAW_ATM, DEPOSIT_TO_OTHER_ACCOUNT_ATM, DEPOSIT_TO_OTHER_CREDITCARD_ATM

from UserManagement.models import AdminBranch, AdminATM
from UserManagement.notification import atm_notification

from .forms import CreateATMForm


def atm_login(request):
    msg = ''
    if request.method == 'POST':
        atm_id = request.POST['atm_id']
        atm_id = int(atm_id)
        print("atm_id: ", atm_id)
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
            try:
                print("Finding ATM...")
                print(atm_id)
                atm = ATM.objects.get(atm_id=atm_id)
                print("ATM Found")

                if creditcard.bank_account.customer.activated:
                    print("CustomerAccount Activated")
                    bankaccount_from = creditcard.bank_account
                    print("BankAccount.Amount: ", bankaccount_from.amount)
                    if bankaccount_from.amount >= amount:

                        if is_withdraw_cash:
                            if atm.amount >= amount:
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
                                msg = 'از کارت شما به شماره کارت {} مبلغ {} برداشته شد.'.format(creditcard.number,
                                                                                                amount)

                                if atm.amount < atm.min_amount:
                                    atm_notification(atm.atm_id)

                            else:
                                msg = 'موجودی خودپرداز کافی نمی‌باشد.'

                        elif is_deposit_to_credit_card:
                            try:
                                print("Finding ToCreditCard...")
                                to_credit_card = CreditCard.objects.get(number=to_credit_card)
                                to_bank_account = to_credit_card.bank_account
                                print("ToCard Found")
                                bankaccount_from.amount -= amount
                                print("NEW BankAccountFrom.Amount: ", bankaccount_from.amount)
                                bankaccount_from.save()
                                print("BankAccountFrom Saved")
                                to_bank_account.amount += amount
                                print("NEW BankAccountTo.Amount: ", to_bank_account.amount)
                                to_bank_account.save()
                                print("BankAccountTo Saved")
                                CreateTansactionModel(bankaccount_from=bankaccount_from,
                                                      branch_from=bankaccount_from.branch,
                                                      bankaccount_to=to_bank_account,
                                                      branch_to=to_bank_account.branch,
                                                      amount=amount,
                                                      type=DEPOSIT_TO_OTHER_CREDITCARD_ATM)
                                print("Transaction Created")
                                msg = 'از کارت شما به شماره کارت {} مبلغ {} به شماره کارت {} واریز شد.'.format(
                                    creditcard.number, amount, to_credit_card.number)
                            except:
                                msg = 'شماره کارت مقصد معتبر نمی‌باشد.'

                        elif is_deposit_to_bank_account:
                            try:
                                print("Finding ToBankAccount...")
                                to_bank_account = BankAccount.objects.get(account_id=to_bank_account)
                                print("ToAccount Found")
                                bankaccount_from.amount -= amount
                                print("NEW BankAccountFrom.Amount: ", bankaccount_from.amount)
                                bankaccount_from.save()
                                print("BankAccountFrom Saved")
                                to_bank_account.amount += amount
                                print("NEW BankAccountTo.Amount: ", to_bank_account.amount)
                                to_bank_account.save()
                                print("BankAccountTo Saved")
                                CreateTansactionModel(bankaccount_from=bankaccount_from,
                                                      branch_from=bankaccount_from.branch,
                                                      bankaccount_to=to_bank_account,
                                                      branch_to=to_bank_account.branch,
                                                      amount=amount,
                                                      type=DEPOSIT_TO_OTHER_ACCOUNT_ATM)
                                print("Transaction Created")
                                msg = 'از کارت شما به شماره کارت {} مبلغ {} به شماره حساب {} واریز شد.'.format(
                                    creditcard.number, amount, to_bank_account.account_id)
                            except:
                                msg = 'شماره کارت مقصد معتبر نمی‌باشد.'
                    else:
                        msg = 'موجودی کارت کافی نمی‌باشد.'
                else:
                    msg = 'حساب کاربری شما غیر فعال می‌باشد.'
            except:
                msg = 'خودپرداز مورد نظر یافت نشد!'
        except:
            msg = 'شماره کارت/رمز عبور اشتباه است.'

    context = {'msg': msg}
    return render(request, 'atm_index.html', context)


@login_required(login_url='/user/login/')
def create_atm(request):
    msg = ''
    try:
        branchadmin = AdminBranch.objects.get(user__user=request.user)
        branch = branchadmin.user.branch
        # managers = AdminATM.objects.all().filter(user__branch=branch)
        managers = AdminATM.objects.all()
        print("Managers Found ", len(managers))

        if request.method == 'POST':
            form = CreateATMForm(request.POST)

            if form.is_valid():
                manager_id = form.cleaned_data.get('manager_id')
                amount = form.cleaned_data.get('amount')
                min_amount = form.cleaned_data.get('min_amount')

                manager = AdminATM.objects.get(user__user__username=manager_id)
                while True:
                    try:
                        atm_id = random_with_N_digits(4)
                        atm = ATM.objects.create(atm_id=atm_id, branch=branch, manager=manager, amount=amount,
                                                 min_amount=min_amount)
                        break
                    except:
                        pass
                manager_full_name = atm.manager.user.user.get_full_name()
                msg = 'خود پرداز شماره {} با موجودی {} تومان و مدیریت {} ساخته شد.'.format(atm.atm_id, atm.amount,
                                                                                           manager_full_name)
        else:
            form = CreateATMForm()
        context = {'form': form,
                   'message': msg,
                   'managers': managers}
        return render(request, 'atm_create.html', context=context)

    except:
        return redirect(reverse('403'))
