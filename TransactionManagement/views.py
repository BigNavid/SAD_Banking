from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from TransactionManagement.forms import WithdrawForm, DepositForm, DepositToOtherForm
from UserManagement.models import Cashier, Accountant
from .models import Transaction


@login_required(login_url='/user/login/')
def withdraw_from_bank_account(request):
    message = ''
    try:
        cashier = Cashier.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = WithdrawForm(request.POST)

            if form.is_valid():
                form.save(cashier)
                bank_account_id = form.cleaned_data.get('bank_account_id')
                amount = form.cleaned_data.get('amount')
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
                form.save(cashier)
                bank_account_id = form.cleaned_data.get('bank_account_id')
                amount = form.cleaned_data.get('amount')
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
                form.save(cashier)
                source_bank_account_id = form.cleaned_data.get('source_bank_account_id')
                destination_bank_account_id = form.cleaned_data.get('destination_bank_account_id')
                amount = form.cleaned_data.get('amount')
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
def accountant_report(request):
    msg = ''
    try:
        accountant = Accountant.objects.get(user__user__username=request.user.username)
        print("User Found")
        branch = accountant.user.branch
        print("Branch Found")

        transactions_from = None
        try:
            transactions_from = Transaction.objects.get(branch_from=branch)
        except:
            print("No Transaction From")
            msg += 'تراکنش خروجی برای این شعبه یافت نشد.\n'

        transactions_to = None
        try:
            transactions_to = Transaction.objects.get(branch_from=branch)
        except:
            print("No Transaction To")
            msg += 'تراکنش ورودی برای این شعبه یافت نشد.'

        print("Hi")
        amount_from = 0
        amount_to = 0
        print("Before For#1")
        if transactions_from is not None:
            for transaction in transactions_from:
                amount = transaction.amount
                amount_from += amount
        print("After For#1")
        if transactions_to is not None:
            for transaction in transactions_to:
                amount = transaction.amount
                amount_to += amount
        print("Bye")
        context = {
            'branch': branch,
            'transactions_to': transactions_to,
            'transactions_from': transactions_from,
            'amount_from': amount_from,
            'amount_to': amount_to
        }

        print("Before Rendering")
        return render(request, 'accountant_report.html', context=context)
    except:
        print("FUCK")
        return redirect(reverse('403'))
