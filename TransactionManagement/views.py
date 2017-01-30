from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from TransactionManagement.forms import WithdrawForm, DepositForm, DepositToOtherForm
from UserManagement.models import Cashier


@login_required(login_url='/user/login/')
def withdraw_from_bank_account(request):
    message = ''
    try:
        cashier = Cashier.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = WithdrawForm(request.POST)

            if form.is_valid():
                form.save()
                bank_account = form.cleaned_data.get('bank_account')
                amount = form.cleaned_data.get('amount')
                message = "از حساب بانکی با شماره حساب {} مبلغ {} کسر شد.".format(
                    bank_account.account_id,
                    amount)
                # return redirect(reverse(''))
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
                bank_account = form.cleaned_data.get('bank_account')
                amount = form.cleaned_data.get('amount')
                message = "به حساب بانکی با شماره حساب {} مبلغ {} اضافه شد.".format(
                    bank_account.account_id,
                    amount)
                # return redirect(reverse(''))
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
                source_bank_account = form.cleaned_data.get('source_bank_account')
                destination_bank_account = form.cleaned_data.get('destination_bank_account')
                amount = form.cleaned_data.get('amount')
                message = "از حساب بانکی با شماره حساب {} مبلغ {} کسر و به حساب بانکی {} اضافه شد.".format(
                    source_bank_account.account_id,
                    amount,
                    destination_bank_account)
                # return redirect(reverse(''))
        else:
            form = WithdrawForm()
        context = {'form': form,
                   'message': message,
                   'cashier': cashier,
                   'username': request.user.username}
        return render(request, 'deposit_to_other_bank_account.html', context=context)
    except:
        return redirect(reverse('TestView'))
