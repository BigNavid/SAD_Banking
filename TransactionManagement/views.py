from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from TransactionManagement import Constants
from TransactionManagement.Utils import CreateTansactionModel
from TransactionManagement.forms import WithdrawForm, DepositForm, DepositToOtherForm, BillPaymentForm, AccountantReportForm
from UserManagement.models import Cashier, Accountant
from .models import Transaction, BankAccount, Bills


@login_required(login_url='/user/login/')
def withdraw_from_bank_account(request):
    message = ''
    try:
        cashier = Cashier.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = WithdrawForm(request.POST)

            if form.is_valid():
                form.save()
                bank_account_id = form.cleaned_data.get('bank_account_id')
                amount = form.cleaned_data.get('amount')
                bankaccount_to = BankAccount.objects.get(account_id=bank_account_id)
                CreateTansactionModel(bankaccount_to=bankaccount_to,
                                      branch_to=bankaccount_to.branch,
                                      amount=amount,
                                      type=Constants.CASH_WITHDRAW,
                                      cashier=cashier)
                message = "از حساب بانکی با شماره حساب {} مبلغ {} کسر شد.".format(
                    bank_account_id,
                    amount)
        else:
            form = WithdrawForm()
        context = {'form': form,
                   'message': message,
                   'cashier': cashier,
                   'username': request.user.username}
        return render(request, 'withdraw_from_bank_account.html', context=context)
    except:
        return redirect(reverse('TestView'))


@login_required(login_url='/user/login/')
def deposit_to_bank_account(request):
    message = ''
    try:
        cashier = Cashier.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = DepositForm(request.POST)

            if form.is_valid():
                form.save()
                bank_account_id = form.cleaned_data.get('bank_account_id')
                amount = form.cleaned_data.get('amount')
                bankaccount_from = BankAccount.objects.get(account_id=bank_account_id)
                CreateTansactionModel(bankaccount_from=bankaccount_from,
                                      branch_from=bankaccount_from.branch,
                                      amount=amount,
                                      type=Constants.CASH_DEPOSIT,
                                      cashier=cashier)
                message = "به حساب بانکی با شماره حساب {} مبلغ {} اضافه شد.".format(
                    bank_account_id,
                    amount)
        else:
            form = WithdrawForm()
        context = {'form': form,
                   'message': message,
                   'cashier': cashier,
                   'username': request.user.username}
        return render(request, 'deposit_to_bank_account.html', context=context)
    except:
        return redirect(reverse('TestView'))


@login_required(login_url='/user/login/')
def deposit_to_other_bank_account(request):
    message = ''
    try:
        cashier = Cashier.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = DepositToOtherForm(request.POST)

            if form.is_valid():
                form.save()
                source_bank_account_id = form.cleaned_data.get('source_bank_account_id')
                destination_bank_account_id = form.cleaned_data.get('destination_bank_account_id')
                amount = form.cleaned_data.get('amount')
                bankaccount_from = BankAccount.objects.get(account_id=source_bank_account_id)
                bankaccount_to = BankAccount.objects.get(account_id=destination_bank_account_id)
                CreateTansactionModel(bankaccount_from=bankaccount_from,
                                      branch_from=bankaccount_from.branch,
                                      bankaccount_to=bankaccount_to,
                                      branch_to=bankaccount_to.branch,
                                      amount=amount,
                                      type=Constants.DEPOSIT_TO_OTHER_ACCOUNT,
                                      cashier=cashier)
                message = "از حساب بانکی با شماره حساب {} مبلغ {} کسر و به حساب بانکی {} اضافه شد.".format(
                    source_bank_account_id,
                    amount,
                    destination_bank_account_id)
        else:
            form = WithdrawForm()
        context = {'form': form,
                   'message': message,
                   'cashier': cashier,
                   'username': request.user.username}
        return render(request, 'deposit_to_other_bank_account.html', context=context)
    except:
        return redirect(reverse('TestView'))

@login_required(login_url='/user/login/')
def bill_payment(request):
    message = ''
    try:
        cashier = Cashier.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = BillPaymentForm(request.POST)

            if form.is_valid():
                form.save()
                bill_id = form.cleaned_data.get('bill_id')
                amount = form.cleaned_data.get('amount')
                bank_account_id = form.cleaned_data.get('bank_account_id')
                bill_kind = form.cleaned_data.get('bill_kind')
                bill_account = Bills.objects.get(kind=bill_kind).BankAccount_to
                bank_account = BankAccount.objects.get(account_id=bank_account_id)
                CreateTansactionModel(bankaccount_from=bank_account,
                                      branch_from=bank_account.branch,
                                      bankaccount_to=bill_account,
                                      branch_to=bill_account.branch,
                                      amount=amount,
                                      type=Constants.BILL_PAYEMENT,
                                      cashier=cashier)
                message = "قبض {} با شماره {} و مبلغ {} پرداخت شد.".format(
                    bill_kind,
                    bill_id,
                    amount)
        else:
            form = BillPaymentForm()
        context = {'form': form,
                   'message': message,
                   'bill_kinds': Bills.objects.all(),
                   'username': request.user.username}
        return render(request, 'bill_payment.html', context=context)
    except:
        return redirect(reverse('TestView'))


@login_required(login_url='/user/login/')
def accountant_report(request):
    msg = ''
    try:
        accountant = Accountant.objects.get(user__user__username=request.user.username)
        branch = accountant.user.branch

        cashiers = Cashier.objects.all().filter(user__branch=branch)

        transactions_from = None
        transactions_to = None
        amount_from = None
        amount_to = None
        form = None

        if request.method == 'POST':
            form = AccountantReportForm(request.POST)
            if form.is_valid():
                amount_from = 0
                amount_to = 0
                national_id = form.cleaned_data.get('national_id')
                if national_id == -1:
                    isAll = True
                else:
                    isAll=False

                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')

                print(national_id)
                print(start_date)
                print(end_date)
                print(branch.branch_id)

                try:
                    if isAll:
                        transactions_from = Transaction.objects.all().filter(branch_from=branch, date_time__range=[start_date, end_date])
                    else:
                        transactions_from = Transaction.objects.all().filter(branch_from=branch, cashier__user__national_id=national_id,
                                                                             date_time__range=[start_date, end_date])
                except:
                    msg += 'تراکنش خروجی برای این شعبه/صندوقدار یافت نشد.'

                try:
                    if isAll:
                        transactions_to = Transaction.objects.all().filter(branch_to=branch, date_time__range=[start_date, end_date])
                    else:
                        transactions_to = Transaction.objects.all().filter(branch_to=branch, cashier__user__national_id=national_id,
                                                                             date_time__range=[start_date, end_date])
                except:
                    msg += 'تراکنش ورودی برای این شعبه/صندوقدار یافت نشد.'

                if transactions_from is not None:
                    for transaction in transactions_from:
                        amount = transaction.amount
                        amount_from += amount
                if transactions_to is not None:
                    for transaction in transactions_to:
                        amount = transaction.amount
                        amount_to += amount
            else:
                print('Salam')
        context = {
            'msg': msg,
            'branch': branch,
            'cashiers': cashiers,
            'transactions_to': transactions_to,
            'transactions_from': transactions_from,
            'amount_from': amount_from,
            'amount_to': amount_to,
            'form': form
        }
        return render(request, 'accountant_report.html', context=context)
    except:
        return redirect(reverse('403'))
