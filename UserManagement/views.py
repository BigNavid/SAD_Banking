from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from TransactionManagement import Constants
from TransactionManagement.Utils import CreateTansactionModel, CreateLoanPaymentModel
from TransactionManagement.models import CheckLeaf, BankAccount, Loan, Bank
from .forms import SignUpCustomerForm, CreateBankAccountForm, SignUpAdminForm, CreateBranchForm, SignUpBranchAdminForm, \
    SignUpStaffForm, CreateCreditCardForm, BillDefinitionForm, CheckRequestForm, LegalExpertCheckConfirmForm, \
    AccountantCheckConfirmForm, ActivateAccountForm, LoanRequestForm, LoanConfirmationForm, FeeForm, RegularTransfers
from .models import Customer, Cashier, Admin, Branch, AdminBranch, LegalExpert, Accountant, Notifications


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
                form.save(cashier.user.branch)
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
            if form.is_valid():
                form.save()
                bank_account_id = form.cleaned_data.get('bank_account_id')
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
                    kind,
                    bank_account_id)
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
        notifications = Notifications.objects.all().filter(user__username=cashier.user.user.username)
        notif_number = len(notifications)

        context = {'cashier': cashier,
                   'notifications': notifications,
                   'notif_number': notif_number}
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

@login_required(login_url='/user/login/')
def profile_accountant(request, username):
    if request.user.username != username:
        return redirect(reverse('403'))
    try:
        accountant = Accountant.objects.get(user__user__username=username)
        context = {'accountant': accountant}
    except:
        return redirect(reverse('403'))
    return render(request, 'accountant_profile.html', context=context)

@login_required(login_url='/user/login/')
def profile_legal_expert(request, username):
    if request.user.username != username:
        return redirect(reverse('403'))
    try:
        legalexpert = LegalExpert.objects.get(user__user__username=username)
        context = {'legalexpert': legalexpert}
    except:
        return redirect(reverse('403'))
    return render(request, 'legalExpert_profile.html', context=context)

@login_required(login_url='/user/login/')
def check_request(request):
    message = ''
    checkLeafList=[]
    try:
        cashier = Cashier.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = CheckRequestForm(request.POST)
            if form.is_valid():
                checkLeafList=form.save()
                bank_account_id = form.cleaned_data.get('bank_account_id')
                message = "دسته چک برای حساب {} صادر گردید.".format(
                    bank_account_id)
        else:
            form = CheckRequestForm()
        context = {'form': form,
                   'message': message,
                   'CheckLeafList': checkLeafList,
                   'username': request.user.username}
        return render(request, 'check_request.html', context=context)
    except:
        return redirect(reverse('TestView'))

@login_required(login_url='/user/login/')
def legalExpert_check_confirm(request):
    # message = ''
    try:
        legalExpert = LegalExpert.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = LegalExpertCheckConfirmForm(request.POST)
            if form.is_valid():
                checkLeaf_id = form.cleaned_data.get('checkleaf_id')
                checkleaf = CheckLeaf.objects.get(checkleaf_id=checkLeaf_id)
                if "accept" in request.POST:
                    checkleaf.legalExpert_confirmation=True
                    checkleaf.save()
                elif 'reject' in request.POST:
                    checkleaf.used = False
                    checkleaf.save()
                # message = "درخواست شما پس از تایید کارشناس حقوقی و حسابرس انجام خواهد شد."
        else:
            form = LegalExpertCheckConfirmForm()
        checkleafes = CheckLeaf.objects.all().filter(used=True, legalExpert_confirmation=False)
        context = {'form': form,
                   'checkleafes': checkleafes,
                   'username': request.user.username}
        return render(request, 'legalExpert_check_confirm.html', context=context)
    except:
        return redirect(reverse('TestView'))

@login_required(login_url='/user/login/')
def accountant_check_confirm(request):
    # message = ''
    try:
        accountant = Accountant.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = AccountantCheckConfirmForm(request.POST)
            if form.is_valid():
                checkLeaf_id = form.cleaned_data.get('checkleaf_id')
                checkleaf = CheckLeaf.objects.get(checkleaf_id=checkLeaf_id)
                if "accept" in request.POST:
                    checkleaf.accountant_confirmation = True
                    bank_account_id = checkleaf.bankaccount_to
                    bank_account = BankAccount.objects.get(account_id=bank_account_id)
                    bank_account.amount -= checkleaf.amount
                    CreateTansactionModel(bankaccount_to=bank_account,
                                          branch_to=bank_account.branch,
                                          amount=checkleaf.amount,
                                          type=Constants.CHECK_PAYMANT,
                                          cashier=checkleaf.cashier)
                    bank_account.save()
                    checkleaf.save()
                elif 'reject' in request.POST:
                    checkleaf.used = False
                    checkleaf.legalExpert_confirmation = False
                    checkleaf.save()
        else:
            form = AccountantCheckConfirmForm()
        checkleafes = CheckLeaf.objects.all().filter(used=True, legalExpert_confirmation=True, accountant_confirmation=False)
        context = {'form': form,
                   'checkleafes': checkleafes,
                   'username': request.user.username}
        return render(request, 'accountant_check_confirm.html', context=context)
    except:
        return redirect(reverse('TestView'))


@login_required(login_url='/user/login/')
def legalExpert_loan_confirm(request):
    # message = ''
    try:
        legalExpert = LegalExpert.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = LoanConfirmationForm(request.POST)
            if form.is_valid():
                loan_id = form.cleaned_data.get('loan_id')
                loan = Loan.objects.get(loan_id=loan_id)
                if "accept" in request.POST:
                    loan.legalExpert_confirmation = True
                    loan.save()
                elif 'reject' in request.POST:
                    loan.reject = True
                    loan.save()
                    # message = "درخواست شما پس از تایید کارشناس حقوقی و حسابرس انجام خواهد شد."
        else:
            form = LoanConfirmationForm()
        loans = Loan.objects.all().filter(reject=False, legalExpert_confirmation=False)
        context = {'form': form,
                   'loans': loans,
                   'username': request.user.username}
        return render(request, 'legalExpert_loan_confirmation.html', context=context)
    except:
        return redirect(reverse('TestView'))


@login_required(login_url='/user/login/')
def accountant_loan_confirm(request):
    # message = ''
    try:
        accountant = Accountant.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = LoanConfirmationForm(request.POST)
            if form.is_valid():
                loan_id = form.cleaned_data.get('loan_id')
                loan = Loan.objects.get(loan_id=loan_id)
                if "accept" in request.POST:
                    loan.accountant_confirmation = True
                    bank_account_id = loan.bank_account
                    bank_account = BankAccount.objects.get(account_id=bank_account_id)
                    FA_bank_account = BankAccount.objects.get(account_id=Constants.FA_BANK_ACCOUNT)
                    bank_account.amount += loan.amount
                    FA_bank_account.amount -= loan.amount
                    CreateTansactionModel(bankaccount_to=bank_account,
                                          branch_to=bank_account.branch,
                                          amount=loan.amount,
                                          type=Constants.LOAN_PAYMANT,
                                          cashier=loan.cashier,
                                          bankaccount_from=FA_bank_account,
                                          branch_from=FA_bank_account.branch)
                    CreateLoanPaymentModel(loan)
                    bank_account.save()
                    FA_bank_account.save()
                    loan.save()
                elif 'reject' in request.POST:
                    loan.reject = True
                    loan.legalExpert_confirmation = False
                    loan.save()
        else:
            form = LoanConfirmationForm()
        loans = Loan.objects.all().filter(reject=False, legalExpert_confirmation=True, accountant_confirmation=False)
        FA_bank_account = BankAccount.objects.get(account_id=Constants.FA_BANK_ACCOUNT)
        FA_amount = FA_bank_account.amount
        context = {'form': form,
                   'loans': loans,
                   'FA_amount': FA_amount,
                   'username': request.user.username}
        return render(request, 'accountant_loan_confirm.html', context=context)
    except:
        return redirect(reverse('TestView'))


@login_required(login_url='/user/login/')
def activate_account(request):
    try:
        legalExpert = LegalExpert.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = ActivateAccountForm(request.POST)
            if form.is_valid():
                customer_username = form.cleaned_data.get('customer_username')
                customer = Customer.objects.get(user__username=customer_username)
                if "activate" in request.POST:
                    customer.activated=True
                    customer.save()
                elif 'block' in request.POST:
                    customer.activated=False
                    customer.save()
        else:
            form = ActivateAccountForm()
        customers = Customer.objects.all()
        context = {'form': form,
                   'customers': customers,
                   'username': request.user.username}
        return render(request, 'activate_account.html', context=context)
    except:
        return redirect(reverse('TestView'))


@login_required(login_url='/user/login/')
def loan_request(request):
    message = ''
    try:
        cashier = Cashier.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = LoanRequestForm(request.POST)

            if form.is_valid():
                form.save(cashier)
                message = "وام شما پس از تایید کارشناس حقوقی و حسابرس پرداخت خواهد شد."
        else:
            form = LoanRequestForm()
        bank_accounts = BankAccount.objects.all().filter(customer__activated=True)
        context = {'form': form,
                   'message': message,
                   'bank_accounts': bank_accounts,
                   'username': request.user.username}
        return render(request, 'loan_request.html', context=context)
    except:
        return redirect(reverse('TestView'))


@login_required(login_url='/user/login/')
def fee(request):
    message = ''
    try:
        admin = Admin.objects.get(user__username=request.user.username)
        if request.method == 'POST':
            form = FeeForm(request.POST)
            if form.is_valid():
                form.save()
                message = "کارمزدها و سود بانکی بروز شد."
        else:
            form = FeeForm()
        bank = Bank.objects.get(name="FaBank")
        context = {'form': form,
                   'message': message,
                   'bank': bank,
                   'username': request.user.username}
        return render(request, 'fee.html', context=context)
    except:
        return redirect(reverse('TestView'))


@login_required(login_url='/user/login/')
def regular_transaction(request):
    message = ''
    try:
        Cashier.objects.get(user__user__username=request.user.username)
        if request.method == 'POST':
            form = RegularTransfers(request.POST)
            if form.is_valid():
                form.save()
                rt = form.cleaned_data.get('regular_transaction')
                message = 'حواله منظم شماره {} ساخته شد.'.format(rt.regular_trasaction_id)
        else:
            form = RegularTransfers()

        context = {'form': form,
                   'message': message,
                   'username': request.user.username}
        return render(request, 'regular_transactions_create.html', context=context)
    except:
        return redirect(reverse('TestView'))


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
