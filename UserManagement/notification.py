from TransactionManagement.Constants import CASH_DEPOSIT, CASH_WITHDRAW, DEPOSIT_TO_OTHER_ACCOUNT, BILL_PAYEMENT
from TransactionManagement.models import Transaction, ATM, LoanPayment
from UserManagement.models import Notifications, Admin, AdminBranch


def customer_notification(t_type, t_id):
    if t_type is CASH_DEPOSIT:
        cash_deposit_notif(t_id)
    elif t_type is CASH_WITHDRAW:
        cash_withdraw_notif(t_id)
    elif t_type is DEPOSIT_TO_OTHER_ACCOUNT:
        deposit_to_other_account_notif(t_id)
    elif t_type is BILL_PAYEMENT:
        bill_payment_notif(t_id)


def atm_notification(atm_id):
    atm = ATM.objects.get(atm_id=atm_id)
    user = atm.manager.user.user
    msg = 'دستگاه خودپرداز شماره {} با موجودی {} به آستانه حداقلی خود رسیده است.'.format(atm.atm_id, atm.amount)
    Notifications.objects.create(user=user, message=msg)


def loan_payment_notification(paid, loan_payment_id):
    if paid:
        loan_payment_paid_notif(loan_payment_id=loan_payment_id)
    else:
        loan_payment_not_paid_notif(loan_payment_id=loan_payment_id)


def loan_payment_paid_notif(loan_payment_id):
    loan_payment = LoanPayment.objects.get(loanpayment_id=loan_payment_id)
    loan_id = loan_payment.loadn_id
    customer_full_name = loan_payment.customer.user.get_full_name()
    #TODO: Add account number
    msg = 'مشتری گرامی {} قسط وام شماره {} شماره قسط {} از حساب شما کسر گردید.'.format(customer_full_name, loan_id,
                                                                                       loan_payment_id)
    user = loan_payment.customer.user
    Notifications.objects.create(user=user, message=msg)


def loan_payment_not_paid_notif(loan_payment_id):
    loan_payment = LoanPayment.objects.get(loanpayment_id=loan_payment_id)
    loan_id = loan_payment.loadn_id
    customer_full_name = loan_payment.customer.user.get_full_name()
    msg = 'مشتری گرامی {} قسط وام شماره {} شماره قسط {} پرداخت نشده است.'.format(customer_full_name,
                                                                                 loan_id,
                                                                                 loan_payment_id)
    user = loan_payment.customer.user
    Notifications.objects.create(user=user, message=msg)

    admin = Admin.objects.all()
    msg = 'مدیر محترم فا بانک مشتری {} قسط وام شماره {} شماره قسط {} را پرداخت کرده است.'.format(customer_full_name,
                                                                                                 loan_id,
                                                                                                 loan_payment_id)
    for user in admin:
        Notifications.objects.create(user=user, message=msg)

    #TODO: Get Admin of branch
    branch_admin = AdminBranch.objects.get()
    user = branch_admin.user.user
    msg = 'مدیرشعبه محترم شعبه {} مشتری {} قسط وام شماره {} شماره قسط {} را پرداخت کرده است.'.format(branch_admin.user
                                                                                                     .branch_id,
                                                                                                     customer_full_name,
                                                                                                     loan_id,
                                                                                                     loan_payment_id)
    Notifications.objects.create(user=user, message=msg)
    pass
def cash_deposit_notif(t_id):
    transaction = Transaction.objects.get(transaction_id=t_id)
    msg = 'مبلغ {} تومان به صورت نقدی به حساب شما به شماره حساب {} واریز شد.'.format(transaction.amount, transaction.
                                                                                     bankaccount_to.account_id)
    user = transaction.bankaccount_to.customer.user
    Notifications.objects.create(user=user, message=msg)


def cash_withdraw_notif(t_id):
    transaction = Transaction.objects.get(transaction_id=t_id)
    msg = 'مبلغ {} تومان به صورت نقدی از حساب شما به شماره حساب {} برداشته شد.'.format(transaction.amount,
                                                                     transaction.bankaccount_from.account_id)
    user = transaction.bankaccount_from.customer.user
    Notifications.objects.create(user=user, message=msg)


def deposit_to_other_account_notif(t_id):
    transaction = Transaction.objects.get(transaction_id=t_id)
    msg = 'مبلغ {} تومان از حساب شما به شماره حساب {} به حساب {} واریز شد.'.format(transaction.amount,
                                                                                   transaction.bankaccount_from.
                                                                                   account_id, transaction.
                                                                                   bankaccount_to.account_id)
    user = transaction.bankaccount_from.customer.user
    Notifications.objects.create(user=user, message=msg)

    msg = 'مبلغ {} تومان به حساب شما به شماره حساب {} از حساب {} واریز شد.'.format(transaction.amount,
                                                                                   transaction.bankaccount_to.
                                                                                   account_id, transaction.
                                                                                   bankaccount_from.account_id)
    user = transaction.bankaccount_to.customer.user
    Notifications.objects.create(user=user, message=msg)


def bill_payment_notif(t_id):
    pass
