from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from .forms import SignUpCustomerForm, CreateBankAccountForm, SignUpAdminForm, CreateBranchForm, SignUpBranchAdminForm, \
    SignUpStaffForm, CreateCreditCardForm, BillDefinitionForm
from .models import Customer, Cashier, Admin, Branch, AdminBranch


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
                try:
                    Customer.objects.get(user__username=username)
                    return redirect(reverse('ProfileCustomer', args={username}))
                except:
                    try:
                        Admin.objects.get(user__username=username)
                        return redirect(reverse('ProfileAdmin', args={username}))
                    except:
                        try:
                            AdminBranch.objects.get(user__user__username=username)
                            return redirect(reverse('ProfileBranchAdmin', args={username}))
                        except:
                            return redirect(reverse('TestView', args={username}))

        else:
            error = 'شماره مشتری/پرسنلی یا رمز عبور اشتباه است.'
    context = {'error': error}
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('Login'))


@login_required(login_url='/user/login/')
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


@login_required(login_url='/user/login/')
def signup_admin(request):
    message = ''
    if request.user.is_superuser:
        if request.method == 'POST':
            form = SignUpAdminForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('user')
                message = "حساب کاربری با شماره پرسنلی {} برای کاربر ساخته شد.".format(user.username)
                # return redirect(reverse(''))
        else:
            form = SignUpAdminForm()
        context = {'form': form,
                   'message': message,
                   'username': request.user.username}
        return render(request, 'signup_admin.html', context=context)
    else:
        return redirect(reverse('TestView'))


@login_required(login_url='/user/login/')
def create_branch_admin(request):
    message = ''
    try:
        Admin.objects.get(user__username=request.user.username)
        if request.method == 'POST':
            form = SignUpBranchAdminForm(request.POST)

            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('user')
                message = "حساب کاربری مدیر شعبه به شماره {} ساخته شد.".format(
                    user.username)
                # return redirect(reverse(''))
        else:
            form = SignUpBranchAdminForm()
        context = {'form': form,
                   'message': message,
                   'username': request.user.username,
                   # 'range' : Branch.objects.all(),
                   'branches': Branch.objects.all()}
        return render(request, 'create_branch_admin.html', context=context)
    except:
        return redirect(reverse('TestView'))

@login_required(login_url='/user/login/')
def signup_staff(request):
    message = ''
    try:
        adminBranch=AdminBranch.objects.get(user__user__username=request.user.username)
        Branch=adminBranch.user.branch
        if request.method == 'POST':
            form = SignUpStaffForm(request.POST)
            if form.is_valid():
                form.save(Branch)
                user = form.cleaned_data.get('user')
                message = "حساب کاربری کارمند به شماره پرسنلی {} ساخته شد.".format(
                    user.username)
                # return redirect(reverse(''))
        else:
            form = SignUpStaffForm()
        context = {'form': form,
                   'message': message,
                   'username': request.user.username}
                   # 'range' : Branch.objects.all(),
                   # 'branches': Branch.objects.all()}
        return render(request, 'signup_staff.html', context=context)
        # return redirect(reverse('SignupStaff', args={username}), context = context)
    except:
        return redirect(reverse('TestView'))

@login_required(login_url='/user/login/')
def create_branch(request):
    message = ''
    try:
        Admin.objects.get(user__username=request.user.username)
        if request.method == 'POST':
            form = CreateBranchForm(request.POST)

            if form.is_valid():
                form.save()
                branch = form.cleaned_data.get('branch')
                message = "شعبه به شماره {} ساخته شد.".format(
                    branch.branch_id)
                # return redirect(reverse(''))
        else:
            form = CreateBranchForm()
        context = {'form': form,
                   'message': message,
                   'username': request.user.username}
        return render(request, 'create_branch.html', context=context)
    except:
        return redirect(reverse('TestView'))


@login_required(login_url='/user/login/')
def create_bank_account(request):
    message = ''
    try:
        cashier = Cashier.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = CreateBankAccountForm(request.POST)

            if form.is_valid():
                form.save(cashier.branch)
                bank_account = form.cleaned_data.get('bank_account')
                message = "حساب بانکی با شماره حساب {} برای مشتری ساخته شد.".format(
                    bank_account.account_id)
                # return redirect(reverse(''))
        else:
            form = CreateBankAccountForm()
        context = {'form': form,
                   'message': message,
                   'cashier': cashier,
                   'username': request.user.username}
        return render(request, 'create_bank_account.html', context=context)
    except:
        return redirect(reverse('TestView'))

@login_required(login_url='/user/login/')
def create_creditcard(request):
    message = ''
    try:
        cashier = Cashier.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = CreateCreditCardForm(request.POST)
            bank_account_id = form.cleaned_data.get('bank_account_id')
            if form.is_valid():
                form.save()
                credit_card= form.cleaned_data.get('credit_card')
                message = "کارت بانکی با شماره {} برای حساب شماره {} صادر شد.".format(
                    credit_card.number,
                    bank_account_id)
                # return redirect(reverse(''))
        else:
            form = CreateCreditCardForm()
        context = {'form': form,
                   'message': message,
                   'username': request.user.username}
        return render(request, 'create_credit_card.html', context=context)
    except:
        return redirect(reverse('TestView'))

@login_required(login_url='/user/login/')
def bill_definition(request):
    message = ''
    try:
        admin = Admin.objects.get(user__username=request.user.username)
        if request.method == 'POST':
            form = BillDefinitionForm(request.POST)

            if form.is_valid():
                form.save()
                bank_account_id = form.cleaned_data.get('bank_account_id')
                kind = form.cleaned_data.get('kind')
                message = "قبض {} با شماره حساب {} تعریف شد.".format(
                    bank_account_id,
                    kind)
        else:
            form = BillDefinitionForm()
        context = {'form': form,
                   'message': message,
                   'username': request.user.username}
        return render(request, 'bill_definition.html', context=context)
    except:
        return redirect(reverse('TestView'))

@login_required(login_url='/user/login/')
def profile_customer(request, username):
    if request.user.username != username:
        return redirect(reverse('403'))
    try:
        customer = Customer.objects.get(user__username=username)
        context = {'customer': customer}
    except:
        return redirect(reverse('403'))
    return render(request, 'customer_profile.html', context=context)


@login_required(login_url='/user/login/')
def test(request, username):
    if request.user.username != username:
        return redirect(reverse('403'))
    customer = User.objects.get(username=username)
    context = {'customer': customer}
    return render(request, 'Test.html', context=context)


@login_required(login_url='/user/login/')
def profile_cashier(request, username):
    if request.user.username != username:
        return redirect(reverse('403'))
    try:
        cashier = Cashier.objects.get(user__user__username=username)
        context = {'cashier': cashier}
    except:
        return redirect(reverse('403'))
    return render(request, 'cashier_profile.html', context=context)


@login_required(login_url='/user/login/')
def profile_admin(request, username):
    if request.user.username != username:
        return redirect(reverse('403'))
    try:
        admin = Admin.objects.get(user__username=username)
        context = {'admin': admin}
    except:
        return redirect(reverse('403'))
    return render(request, 'admin_profile.html', context=context)

@login_required(login_url='/user/login/')
def profile_branch_admin(request, username):
    if request.user.username != username:
        return redirect(reverse('403'))
    try:
        adminBranch = AdminBranch.objects.get(user__user__username=username)
        context = {'adminBranch': adminBranch}
    except:
        return redirect(reverse('403'))
    return render(request, 'branch_admin_profile.html', context=context)


def forbidden(request):
    return render(request, '403.html')


def ghabz(request):
    cashier = Cashier.objects.get(user__user__username=request.user.username)
    context = {'cashier': cashier,
               'username': request.user.username}
    return render(request, 'ghabz.html', context=context)


def vam(request):
    cashier = Cashier.objects.get(user__user__username=request.user.username)
    context = {'cashier': cashier,
               'username': request.user.username}
    return render(request, 'vam.html', context=context)


def check(request):
    cashier = Cashier.objects.get(user__user__username=request.user.username)
    context = {'cashier': cashier,
               'username': request.user.username}
    return render(request, 'check.html', context=context)


def gozaresh(request):
    cashier = Cashier.objects.get(user__user__username=request.user.username)
    context = {'cashier': cashier,
               'username': request.user.username}
    return render(request, 'gozaresh.html', context=context)


def havale_monazam(request):
    cashier = Cashier.objects.get(user__user__username=request.user.username)
    context = {'cashier': cashier,
               'username': request.user.username}
    return render(request, 'havale.html', context=context)


def gardesh_hesab(request):
    cashier = Cashier.objects.get(user__user__username=request.user.username)
    context = {'cashier': cashier,
               'username': request.user.username}
    return render(request, 'ghardesh.html', context=context)


def tarif_eskenas(request):
    cashier = Cashier.objects.get(user__user__username=request.user.username)
    context = {'cashier': cashier,
               'username': request.user.username}
    return render(request, 'atm_eskenas.html', context=context)


def masdodsazi(request):
    cashier = Cashier.objects.get(user__user__username=request.user.username)
    context = {'cashier': cashier,
               'username': request.user.username}
    return render(request, 'masdod.html', context=context)


def faalsazi(request):
    cashier = Cashier.objects.get(user__user__username=request.user.username)
    context = {'cashier': cashier,
               'username': request.user.username}
    return render(request, 'faalsazi.html', context=context)


def hesabbehesab(request):
    cashier = Cashier.objects.get(user__user__username=request.user.username)
    context = {'cashier': cashier,
               'username': request.user.username}
    return render(request, 'hesabbehesab.html', context=context)
