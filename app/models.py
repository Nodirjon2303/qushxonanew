import datetime

import django
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name



class Client(models.Model):
    full_name  =models.CharField(max_length=250, null=True, blank=True)
    address = models.CharField(max_length=225, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    role = models.CharField(max_length=125, null=True, blank=True, choices=[
        ('dehqon', 'Dehqon'),
        ('client', 'Qushxona Klienti(Sotib oluvhi)'),
        ('sotuvchi', "Bozordagi sotuvchi"),
        ('kallahasb', 'Kalla hasb oluvchi sotuvchi'),
        ('Teri', 'Teri oluvchi sotuvchi')
    ])
    status_bozor = models.BooleanField(default=False, null=True, blank=True)
    def __str__(self):
        return f"{self.full_name}"
class  ExpenseDehqon(models.Model):
    dehqon = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=125, null=True, blank=True, choices=[('progress', 'Jarayonda'), ('completed', 'Yakunlandi')], default='progress')
    def __str__(self):
        return f"{self.dehqon.full_name} {self.created_date}"




class IncomeClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='qaysi client oldi+')
    product_dehqon = models.ForeignKey(ExpenseDehqon, on_delete=models.SET_NULL, null=True, related_name='qaysi dehqonni qoyi+')
    quantity = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True, default=0)
    price = models.IntegerField(null=True, blank=True, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=125, null=True, blank=True, choices=[('bron', 'Bron qilindi'), ('progress', 'Jarayonda'), ('completed', 'Yakunlandi')], default='progress')
    def __str__(self):
        return f"{self.client.full_name} {self.product_dehqon.product.name} {self.created_date.ctime()}"


class IncomeSotuvchi(models.Model):
    sotuvchi = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=88, null=True, blank=True,choices=[("progress", "Jarayonda"), ("completed", "yakunlandi")] ,default='progress')

    def __str__(self):
        return f"{self.sotuvchi.full_name} {self.product} {self.created_date.ctime()}"

class IncomeDehqon(models.Model):
    dehqon_product = models.ForeignKey(ExpenseDehqon, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dehqon_product.dehqon.full_name}   {self.amount}"

class  ExpenseClient(models.Model):
    amount = models.IntegerField(null=True, blank=True, default=0)
    income_client = models.ForeignKey(IncomeClient, models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.income_client.client.full_name}  {self.amount}  {self.created_date}"

class ExpenseSotuvchi(models.Model):
    income_sotuvchi = models.ForeignKey(IncomeSotuvchi, models.SET_NULL, null=True)
    amount = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.income_sotuvchi.sotuvchi.full_name}  {self.amount}  {self.created_date}"

class KallaHasb(models.Model):
    mijoz = models.ForeignKey(Client, models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, models.SET_NULL, null=True, blank=True)
    soni = models.IntegerField(null=True, blank=True, default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mijoz.full_name}  {self.product.name}"

class Teri(models.Model):
    mijoz = models.ForeignKey(Client, models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, models.SET_NULL, null=True, blank=True)
    soni = models.IntegerField(null=True, blank=True, default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mijoz.full_name}  {self.product.name}"


class Xarajat(models.Model):
    comment = models.CharField(max_length=125, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    choise = models.CharField(max_length=125, null=True, blank=True,choices=[("qushxona", "Qushxona uchun xarajat"), ('bozor', 'bozordagi xarajatlar')])


    def __str__(self):
        return self.comment
