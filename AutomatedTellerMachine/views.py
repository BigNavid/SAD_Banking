from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from TransactionManagement.models import CreditCard, ATM, AdminATM
from TransactionManagement.Utils import CreateTansactionModel, random_with_N_digits
from TransactionManagement.Constants import WITHDRAW_ATM, DEPOSIT_TO_OTHER_ACCOUNT_ATM, DEPOSIT_TO_OTHER_CREDITCARD_ATM

from UserManagement.models import AdminBranch, AdminATM

from .forms import CreateATMForm


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

                manager = AdminATM.objects.get(user__user__username=manager_id)
                while True:
                    try:
                        atm_id = random_with_N_digits(4)
                        atm = ATM.objects.create(atm_id=atm_id, branch=branch, manager=manager, amount=amount)
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
