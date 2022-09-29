import datetime

import django
import idna
from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True, verbose_name="Mahsulot nomi")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def __str__(self):
        return self.name


class Client(models.Model):
    full_name = models.CharField(max_length=250, null=True, blank=True, verbose_name="F.I.O")
    address = models.CharField(max_length=225, null=True, blank=True, verbose_name="Manzil")
    phone = models.CharField(max_length=25, null=True, blank=True, verbose_name="Telefon raqami")
    role = models.CharField(max_length=125, null=True, blank=True, choices=[
        ('dehqon', 'Dehqon'),
        ('client', 'Qushxona Klienti(Sotib oluvhi)'),
        ('sotuvchi', "Bozordagi sotuvchi"),
        ('kallahasb', 'Kalla hasb oluvchi sotuvchi'),
        ('Teri', 'Teri oluvchi sotuvchi')
    ], verbose_name="Vazifasi (Clientning roli)")
    status_bozor = models.BooleanField(default=False, null=True, blank=True, verbose_name="Bozor uchun sotuvchi")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.status_bozor and Client.objects.filter(status_bozor=True).count() > 1:
            self.status_bozor = False
            return ValidationError({"status_bozor": "Allaqachon Bozor uchun sotuvchi tanlangan\n"
                                                    "Bozor uchun sotuvchi faqat 1 kishi bo'lishi mumkin!!!"})
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klientlar"

    def __str__(self):
        return f"{self.full_name} {self.role} "


class ExpenseDehqon(models.Model):
    dehqon = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Dehqon", )
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Mahsulot")
    quantity = models.BigIntegerField(null=True, blank=True, verbose_name="Soni")
    weight = models.FloatField(null=True, blank=True, verbose_name="Og'irligi")
    price = models.BigIntegerField(null=True, blank=True, default=0, verbose_name="Narxi")
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=125, null=True, blank=True,
                              choices=[('progress', 'Jarayonda'), ('completed', 'Yakunlandi')], default='progress',
                              verbose_name="Holati")
    class Meta:
        verbose_name = "Dehqonning xarajati"
        verbose_name_plural = "Dehqonlarning xarajatlari"

    def __str__(self):
        if self.dehqon:
            return f"{self.dehqon.full_name} {self.created_date}"
        else:
            return f"{self.created_date}"


class IncomeClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True,
                               related_name='qaysi client oldi+', verbose_name="Mijoz")
    product_dehqon = models.ForeignKey(ExpenseDehqon, on_delete=models.SET_NULL, null=True,
                                       related_name='qaysi dehqonni qoyi+' ,blank=True, verbose_name="Dehqonning mahsuloti")
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Soni")
    weight = models.FloatField(null=True, blank=True, default=0, verbose_name="Og'irligi")
    price = models.IntegerField(null=True, blank=True, default=0, verbose_name="Narxi")
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=125, null=True, blank=True,verbose_name="Holati",
                              choices=[('bron', 'Bron qilindi'), ('progress', 'Jarayonda'),
                                       ('completed', 'Yakunlandi')], default='progress')
    class Meta:
        verbose_name = "Klient kirimi"
        verbose_name_plural = "Klientlarning kirimlari"
    def __str__(self):
        title = ""
        if self.client:
            title += f"{self.client.full_name}  "
        if self.product_dehqon and self.product_dehqon.product:
            title += f"  {self.product_dehqon.product.name}"
        title += f"{self.created_date.ctime()}"
        return title


class IncomeSotuvchi(models.Model):
    sotuvchi = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Sotuvchi",)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Mahsulot")
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Soni")
    weight = models.FloatField(null=True, blank=True, verbose_name="Og'irligi")
    price = models.IntegerField(null=True, blank=True, default=0, verbose_name="Narxi")
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=88, null=True, blank=True,
                              choices=[("progress", "Jarayonda"), ("completed", "yakunlandi")], default='progress', verbose_name="Holati")
    class Meta:
        verbose_name = "Sotuvchi kirimi"
        verbose_name_plural = "Sotuvchilar kirimlari"
    def __str__(self):
        return f"{self.sotuvchi} {self.product} {self.created_date.ctime()}"


class IncomeDehqon(models.Model):
    dehqon_product = models.ForeignKey(ExpenseDehqon, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Dehqon mahsuloti")
    amount = models.IntegerField(null=True, blank=True, verbose_name="Miqdori")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Qabul qilib olingan sanasi")
    class Meta:
        verbose_name = "Dehqonga to'langan pullar"
        verbose_name_plural = "Dehqonlarga to'langan pullar"
    def __str__(self):
        if self.dehqon_product and self.dehqon_product.dehqon:
            return f"{self.dehqon_product.dehqon.full_name}   {self.amount}"
        else:
            return f"{self.amount}"


class ExpenseClient(models.Model):
    amount = models.IntegerField(null=True, blank=True, default=0, verbose_name="Miqdori")
    income_client = models.ForeignKey(IncomeClient, models.PROTECT, null=True, blank=True, verbose_name="Klient chiqimi")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Klient chiqimi"
        verbose_name_plural = "Klientlar chiqimlari"

    def __str__(self):
        return f"{self.income_client.client.full_name}  {self.amount}  {self.created_date}"


class ExpenseSotuvchi(models.Model):
    income_sotuvchi = models.ForeignKey(IncomeSotuvchi, models.PROTECT, null=True, blank=True, verbose_name="Sotuvchi chiqimi")
    amount = models.IntegerField(null=True, blank=True,  verbose_name="Miqdori")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Sana")

    class Meta:
        verbose_name = "Sotuvchi chiqimi"
        verbose_name_plural = "Sotuvchilar chiqimlari"
    def __str__(self):
        return f"{self.income_sotuvchi.sotuvchi.full_name}  {self.amount}  {self.created_date}"


class KallaHasb(models.Model):
    mijoz = models.ForeignKey(Client, models.PROTECT, null=True, blank=True, verbose_name="Mijoz")
    product = models.ForeignKey(Product, models.SET_NULL, null=True, blank=True, verbose_name="Mahsulot")
    soni = models.IntegerField(null=True, blank=True, default=0, verbose_name="Soni")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Sana")

    class Meta:
        verbose_name = "Kalla hasb"
        verbose_name_plural = "Kalla hasblar"
    def __str__(self):
        return f"{self.mijoz.full_name}  {self.product.name}"


class Teri(models.Model):
    mijoz = models.ForeignKey(Client, models.PROTECT, null=True, blank=True, verbose_name="Mijoz")
    product = models.ForeignKey(Product, models.SET_NULL, null=True, blank=True, verbose_name="Mahsulot")
    soni = models.IntegerField(null=True, blank=True, default=0, verbose_name="Soni")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Sana")

    def __str__(self):
        return f"{self.mijoz.full_name}  {self.product.name}"


class Xarajat(models.Model):
    comment = models.CharField(max_length=125, null=True, blank=True, verbose_name="Izoh")
    amount = models.IntegerField(null=True, blank=True, default=0, verbose_name="Miqdori")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Sana")
    choise = models.CharField(max_length=125, null=True, blank=True,
                              choices=[("qushxona", "Qushxona uchun xarajat"), ('bozor', 'bozordagi xarajatlar')], verbose_name="Xarajat turi")

    class Meta:
        verbose_name = "Xarajat"
        verbose_name_plural = "Xarajatlar"
    def __str__(self):
        return self.comment
