from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from .forms import SignUpCustomerForm
from .models import Customer


def homepage(request):
    pass


def login_user(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            group = Group.objects.get(name='Cashier')
            if group in request.user.groups.all():
                return redirect(reverse('SignUpCustomer'))
            else:
                return redirect(reverse('TestView', args={username}))
        else:
            error = 'شماره مشتری/پرسنلی ویا رمز عبور اشتباه است.'
    context = {'error': error}
    return render(request, 'login.html', context)


@login_required(login_url='/login')
def signup_customer(request):
    message = ''
    group = Group.objects.get(name='Cashier')
    if group not in request.user.groups.all():
        return redirect(reverse('TestView'))
    if request.method == 'POST':
        form = SignUpCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('user')
            message = """{}
            حساب کاربری با موفقیت ساخته شد.""" \
                .format(user.username)
            # return redirect(reverse(''))
    else:
        form = SignUpCustomerForm()
    context = {'form': form,
               'message': message}
    return render(request, 'SignUpCustomer.html', context=context)


def signup_accountant(request):
    pass


def signup_branchAdmin(request):
    pass


@login_required(login_url='/login')
def profile_customer(request, id):
    customer = Customer.objects.get(number=id)
    context = {'customer': customer}
    return render(request, '', context=context)


@login_required(login_url='/login')
def test(request, username):
    customer = Customer.objects.get(user__username=username)
    context = {'customer': customer}
    return render(request, 'Test.html', context=context)


def logout(request):
    logout(request)
    return redirect(reverse('Login'))
