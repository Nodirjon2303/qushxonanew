import datetime

import django
import idna
import requests
from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True, verbose_name="Mahsulot nomi")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def __str__(self):
        return self.name


class BazarSource(models.Choices):
    bozor = 'bozor'
    qushxona = 'qushxona'


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
        verbose_name = "Dehqonlardan kelgan mol"
        verbose_name_plural = "Dehqonlarning kelgan mollar"

    def __str__(self):
        if self.dehqon:
            return f"{self.dehqon.full_name} {self.created_date}"
        else:
            return f"{self.created_date}"


class IncomeClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True,
                               related_name='qaysi client oldi+', verbose_name="Mijoz")
    product_dehqon = models.ForeignKey(ExpenseDehqon, on_delete=models.SET_NULL, null=True,
                                       related_name='incomeclients', blank=True,
                                       verbose_name="Dehqonning mahsuloti")
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Soni")
    weight = models.FloatField(null=True, blank=True, default=0, verbose_name="Og'irligi")
    price = models.IntegerField(null=True, blank=True, default=0, verbose_name="Narxi")
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=125, null=True, blank=True, verbose_name="Holati",
                              choices=[('bron', 'Bron qilindi'), ('progress', 'Jarayonda'),
                                       ('completed', 'Yakunlandi')], default='progress')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        from app.models import BazarAllIncomeStock
        self.weight = int(self.weight * 10) / 10
        super().save(force_insert, force_update, using, update_fields)
        if self.status in ('progress' or 'completed') and self.client.status_bozor:
            if not BazarAllIncomeStock.objects.filter(
                    remote_id=self.id, source='qushxona').exists():
                BazarAllIncomeStock.objects.create(
                    remote_id=self.id,
                    source='qushxona',
                    product=self.product_dehqon.product,
                    quantity=self.quantity,
                    weight=self.weight,
                    price=self.price,
                    client=self.client,
                )
            else:
                bazar_income = BazarAllIncomeStock.objects.filter(remote_id=self.id, source='qushxona').first()
                bazar_income.client = self.client
                bazar_income.product = self.product_dehqon.product
                bazar_income.quantity = self.quantity
                bazar_income.weight = self.weight
                bazar_income.price = self.price
                bazar_income.save()

    class Meta:
        verbose_name = "Qushxona klienti sotib olgan mahsuloti"
        verbose_name_plural = "Qushxona klienti sotib olgan mahsulolari"

    def __str__(self):
        title = ""
        if self.client:
            title += f"{self.client.full_name}  "
        if self.product_dehqon and self.product_dehqon.product:
            title += f"  {self.product_dehqon.product.name}"
        title += f"{self.created_date.ctime()}"
        return title


class IncomeSotuvchi(models.Model):
    sotuvchi = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Sotuvchi", )
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Mahsulot")
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Soni")
    weight = models.FloatField(null=True, blank=True, verbose_name="Og'irligi")
    price = models.IntegerField(null=True, blank=True, default=0, verbose_name="Narxi")
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=88, null=True, blank=True,
                              choices=[("progress", "Jarayonda"), ("completed", "yakunlandi")], default='progress',
                              verbose_name="Holati")
    source = models.CharField(max_length=125, verbose_name="Manba",
                              choices=BazarSource.choices, default=BazarSource.qushxona)
    class Meta:
        verbose_name = "Bozor sotuvchi sotib olgan mahsuloti"
        verbose_name_plural = "Bozor sotuvchilari sotib olgan mahsulolari"

    def __str__(self):
        return f"{self.sotuvchi} {self.product} {self.created_date.ctime()}"


class IncomeDehqon(models.Model):
    dehqon_product = models.ForeignKey(ExpenseDehqon, on_delete=models.PROTECT, null=True, blank=True,
                                       verbose_name="Dehqon mahsuloti")
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
    income_client = models.ForeignKey(IncomeClient, models.PROTECT, null=True, blank=True,
                                      verbose_name="Klient chiqimi")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Klient to'lovi"
        verbose_name_plural = "Klientlar to'lovlari"

    def __str__(self):
        return f"{self.income_client.client.full_name}  {self.amount}  {self.created_date}"


class IncomeBazarOther(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Mijoz")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Mahsulot")
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Soni")
    weight = models.FloatField(null=True, blank=True, verbose_name="Og'irligi")
    price = models.IntegerField(null=True, blank=True, default=0, verbose_name="Sotib olingan Narxi")
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=88, null=True, blank=True,
                              choices=[("progress", "Jarayonda"), ("completed", "yakunlandi")], default='progress',
                              verbose_name="Holati")
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(IncomeBazarOther, self).save(*args, **kwargs)
        from app.models import BazarAllIncomeStock
        if not BazarAllIncomeStock.objects.filter(remote_id=self.id, source='bazar').exists():
            BazarAllIncomeStock.objects.create(product=self.product, client=self.client, remote_id=self.id,
                                               quantity=self.quantity, weight=self.weight, source='bozor',
                                               price=self.price)
        else:
            bazar = BazarAllIncomeStock.objects.get(source='bozor', remote_id=self.id)
            bazar.client = self.client
            bazar.product = self.product
            bazar.quantity = self.quantity
            bazar.weight = self.weight
            bazar.price = self.price
            bazar.save()

    class Meta:
        verbose_name = "Bozordan ichki mahsulotlar"
        verbose_name_plural = "Bozor ichki mahsulotlari"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.product} {self.quantity} {self.price} {self.created_date}"


class ExpenseSotuvchi(models.Model):
    income_sotuvchi = models.ForeignKey(IncomeSotuvchi, models.PROTECT, null=True, blank=True,
                                        verbose_name="Sotuvchi chiqimi")
    amount = models.IntegerField(verbose_name="Miqdori")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Sana")

    class Meta:
        verbose_name = "Bozor sotuvchilari to'lovi"
        verbose_name_plural = "Bozor sotuvchilari to'lovlari"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super(ExpenseSotuvchi, self).save(force_insert, force_update, using, update_fields)
        try:
            text = f"Sotuvchidan to'lov!!!\n" \
                   f"Sotuvchining ismi: {self.income_sotuvchi.sotuvchi.full_name}\n" \
                   f"Tulov miqdori: {str(self.amount)[:-3] + ' ' + str(self.amount)[-3:]}"
            requests.post(
                f'https://api.telegram.org/bot5262072872:AAFdCPS5Ah7fJV8Qyl-rIxcfw8otYDI6Sr0/sendMessage?chat_id=-1001610927804&text={text}')
        except Exception as e:
            print(e)




    def __str__(self):
        return f"{self.income_sotuvchi}  {self.amount}  {self.created_date}"


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
                              choices=[("qushxona", "Qushxona uchun xarajat"), ('bozor', 'bozordagi xarajatlar')],
                              verbose_name="Xarajat turi")

    class Meta:
        verbose_name = "Boshqa Xarajat"
        verbose_name_plural = "Boshqa Xarajatlar"

    def __str__(self):
        return self.comment


class BazarAllIncomeStock(models.Model):
    product = models.ForeignKey(Product, models.PROTECT, null=True, blank=True, verbose_name="Mahsulot")
    client = models.ForeignKey(Client, models.PROTECT)
    quantity = models.IntegerField(null=True, blank=True, default=0, verbose_name="Soni")
    weight = models.FloatField(null=True, blank=True, default=0, verbose_name="Og'irligi")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Sana")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    remote_id = models.IntegerField(verbose_name="Remote id")
    price = models.IntegerField(verbose_name="Narxi 1kg uchun")
    source = models.CharField(max_length=125, choices=BazarSource.choices, verbose_name="Manba")

    class Meta:
        verbose_name = "Bozorga barcha sotib olingan mahsulotlar"
        verbose_name_plural = "Bozorga barcha sotib olingan mahsulotlar"

    def __str__(self):
        return f"{self.product.name}  {self.quantity}"
