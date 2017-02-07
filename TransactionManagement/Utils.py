import random

from TransactionManagement import Constants
from TransactionManagement.models import Transaction, LoanPayment


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


def CreateTansactionModel(bankaccount_from=None,
                          branch_from=None,
                          bankaccount_to=None,
                          branch_to=None,
                          amount=None,
                          type=None,
                          cashier=None):
    while True:
        try:
            transaction_id = random_with_N_digits(6)
            transaction = Transaction(transaction_id=transaction_id)
            break
        except:
            pass

    transaction.bankaccount_from = bankaccount_from
    transaction.bankaccount_to = bankaccount_to
    transaction.amount = amount
    transaction.cashier = cashier
    transaction.branch_from = branch_from
    transaction.branch_to = branch_to
    transaction.branch = cashier.user.branch
    transaction.type = type
    transaction.save()

def UpdateAmount(bankAccount):
    pass

def CreateLoanPaymentModel(loan):
    amount = loan.amount
    remain = amount % loan.installments
    installment = (amount-remain)/loan.installments
    for i in range(0, loan.installments):
        if i == loan.installments:
            installment += remain
        while True:
            try:
                loanpayment_id = random_with_N_digits(8)
                profit = installment*Constants.LOAN_PROFIT
                LoanPayment.objects.create(loanpayment_id=loanpayment_id,
                                           loan=loan,
                                           amount=installment+profit,
                                           profit=profit)
            except:
                pass