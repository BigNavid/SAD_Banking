from django.contrib import admin

from .models import Fees, BankAccount, Loan, LoanPayment, Money, Bills, Transaction, ATM, ATMMoneys, Check, CheckLeaf, Bank, CreditCard

admin.site.register(Fees)
admin.site.register(BankAccount)
admin.site.register(Loan)
admin.site.register(LoanPayment)
admin.site.register(Money)
admin.site.register(Bills)
# admin.site.register(BillPayment)
admin.site.register(Transaction)
admin.site.register(ATM)
admin.site.register(ATMMoneys)
admin.site.register(Check)
admin.site.register(CheckLeaf)
admin.site.register(Bank)
admin.site.register(CreditCard)

