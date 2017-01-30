from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse


from UserManagement.models import Customer


def atm_login(request):
    msg = ''
    if request.method == 'POST':
        card_number = request.POST['card_number']
        password = request.POST['password']
        try:
            customer = Customer.objects.get(card_number=card_number)
            username = customer.user.username
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('Services'))
            else:
                msg = 'شماره کارت ویا کلمه عبور وارد شده صحیح نمی‌باشد.'
        except:
            msg = 'شماره کارت ویا کلمه عبور وارد شده صحیح نمی‌باشد.'
    context = {'msg': msg}
    return render(request, 'atm_index.html', context)


def choose_service(request):
    return render(request, 'atm_index.html')


def atm_logout(request):
    logout(request)
    return redirect(reverse('ATMLogin'))
