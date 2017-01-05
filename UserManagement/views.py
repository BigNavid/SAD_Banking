from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from .forms import SignUpCustomerForm
from .models import Customer, Cashier


def homepage(request):
    return render(request, 'homepage.html')


def login_user(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                Cashier.objects.get(user__user__username=username)
                return redirect(reverse('ProfileCashier', args={username}))
            except:
                return redirect(reverse('TestView', args={username}))
        else:
            error = 'شماره مشتری/پرسنلی ویا رمز عبور اشتباه است.'
    context = {'error': error}
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('Login'))


@login_required(login_url='/login')
def signup_customer(request):
    message = ''
    try:
        Cashier.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = SignUpCustomerForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('user')
                message = "حساب کاربری با شماره مشتری {} برای کاربر ساخته شد.".format(user.username)
                # return redirect(reverse(''))
        else:
            form = SignUpCustomerForm()
        context = {'form': form,
                   'message': message,
                   'username': request.user.username}
        return render(request, 'signup_customer.html', context=context)
    except:
        return redirect(reverse('TestView'))


def signup_accountant(request):
    pass


def signup_branch_admin(request):
    pass


@login_required(login_url='/login')
def profile_customer(request, id):
    customer = Customer.objects.get(number=id)
    context = {'customer': customer}
    return render(request, '', context=context)


@login_required(login_url='/login')
def test(request, username):
    if request.user.username != username:
        return redirect(reverse('403'))
    customer = User.objects.get(username=username)
    context = {'customer': customer}
    return render(request, 'Test.html', context=context)


@login_required(login_url='/login')
def profile_cashier(request, username):
    if request.user.username != username:
        return redirect(reverse('403'))
    try:
        cashier = Cashier.objects.get(user__user__username=username)
        context = {'cashier': cashier}
    except:
        return redirect(reverse('403'))
    return render(request, 'cashier_profile.html', context=context)


def forbidden(request):
    return render(request, '403.html')
