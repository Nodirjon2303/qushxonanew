from django.contrib import admin

from .models import *

# Register your models here.
# admin.site.register(Product)
# admin.site.register(IncomeClient)
# admin.site.register(IncomeDehqon)
admin.site.register(IncomeSotuvchi)
# admin.site.register(ExpenseDehqon)
admin.site.register(ExpenseSotuvchi)
admin.site.register(ExpenseClient)
admin.site.register(KallaHasb)
admin.site.register(Teri)
admin.site.register(Xarajat)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'role', 'status_bozor']
    search_fields = ['full_name', 'phone']


@admin.register(IncomeClient)
class IncomeClientAdmin(admin.ModelAdmin):
    list_display = ['client', 'product_dehqon', 'quantity', 'weight', 'price', 'status']
    search_fields = ['client__full_name', 'product_dehqon']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name']


@admin.register(IncomeDehqon)
class IncomeDehqonAdmin(admin.ModelAdmin):
    list_display = ['dehqon_product', 'amount', 'created_date']
    search_fields = ['dehqon_product__dehqon__full_name', ]


@admin.register(ExpenseDehqon)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['dehqon', 'product', 'created_date']
    search_fields = ['id', 'dehqon__full_name', 'product__name']
    autocomplete_fields = ['dehqon', ]


@admin.register(IncomeBazarOther)
class IncomeBazarOtherAdmin(admin.ModelAdmin):
    list_display = ['product', 'weight', 'created_date']
    search_fields = ['product', ]
    list_select_related = ['product', ]


@admin.register(BazarAllIncomeStock)
class BazarAllIncomeStockAdmin(admin.ModelAdmin):
    list_display = ['product', 'client', 'weight', 'created_date']
    search_fields = ['product', 'cleint']
    list_select_related = ['product', 'client']

