from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(IncomeClient)
admin.site.register(IncomeDehqon)
admin.site.register(IncomeSotuvchi)
admin.site.register(ExpenseDehqon)
admin.site.register(ExpenseSotuvchi)
admin.site.register(ExpenseClient)
admin.site.register(KallaHasb)
admin.site.register(Teri)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'role']
