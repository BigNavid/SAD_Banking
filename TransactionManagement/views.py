from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from TransactionManagement.forms import WhithdrawForm
from UserManagement.models import Cashier


def atm_login(request):
    pass


@login_required(login_url='/user/login/')
def whithdraw_from_bank_account(request):
    message = ''
    try:
        cashier = Cashier.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = WhithdrawForm(request.POST)

            if form.is_valid():
                form.save()
                bank_account = form.cleaned_data.get('bank_account')
                amount = form.cleaned_data.get('amout')
                message = "از حساب بانکی با شماره حساب {} مبلغ {} کسر شد.".format(
                    bank_account.account_id,
                    amount)
                # return redirect(reverse(''))
        else:
            form = WhithdrawForm()
        context = {'form': form,
                   'message': message,
                   'cashier': cashier,
                   'username': request.user.username}
        return render(request, 'whithdraw_from_bank_account.html', context=context)
    except:
        return redirect(reverse('TestView'))
