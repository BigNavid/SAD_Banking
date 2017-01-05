from django.contrib import admin

from .models import Admin, Branch, BranchStaff, AdminBranch, Accountant, Cashier, LegalExpert, AdminATM, Customer

admin.site.register(Admin)
admin.site.register(Branch)
admin.site.register(BranchStaff)
admin.site.register(AdminBranch)
admin.site.register(Accountant)
admin.site.register(Cashier)
admin.site.register(LegalExpert)
admin.site.register(AdminATM)
admin.site.register(Customer)