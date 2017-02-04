from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse


from TransactionManagement.models import CreditCard


def atm_login(request):
    msg = ''
    if request.method == 'POST':
        cardNumber = request.POST['cardNumber']
        password = request.POST['password']
        try:
            creditcard = CreditCard.objects.get(cardNumber=cardNumber, password=password)
            user = creditcard.bank_account.customer.user
            if creditcard is not None:
                login(request, user)
                return redirect(reverse('Services'))
            else:
                msg = 'شماره کارت ویا کلمه عبور وارد شده صحیح نمی‌باشد.'
        except:
            msg = 'شماره کارت ویا کلمه عبور وارد شده صحیح نمی‌باشد.'
    context = {'msg': msg}
    return render(request, 'atm_index.html', context)


@login_required(login_url='/user/login/')
def choose_service(request):
    print("Services")
    return render(request, 'atm_index.html')


def atm_logout(request):
    logout(request)
    return redirect(reverse('ATMLogin'))
