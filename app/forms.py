from django.db.models import Sum
from django.forms import ModelForm
from .models import IncomeBazarOther, IncomeSotuvchi, IncomeClient, Product, BazarAllIncomeStock, ExpenseClient, \
    ExpenseSotuvchi
from django import forms
from django.forms import ValidationError


class BozorBozorIncomeForm(ModelForm):
    class Meta:
        model = IncomeBazarOther
        fields = ['client', 'product', 'quantity', 'weight', 'price']

    weight = forms.FloatField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].label = 'Mijoz'
        self.fields['product'].label = 'Mahsulot'
        self.fields['quantity'].label = 'Soni'
        self.fields['weight'].label = "Og'irligi"
        self.fields['price'].label = 'Narxi(1 kg)'

        # updating client and product querysets
        self.fields['client'].queryset = self.fields['client'].queryset.filter(role='client').order_by('full_name')
        self.fields['product'].queryset = self.fields['product'].queryset.order_by('name')

        # styling fields
        self.fields['client'].widget.attrs.update({'class': 'form-control'})
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['weight'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})

        # PLACEHOLDER
        self.fields['client'].widget.attrs.update({'placeholder': 'Mijozni tanlang'})
        self.fields['product'].widget.attrs.update({'placeholder': 'Mahsulotni tanlang'})
        self.fields['quantity'].widget.attrs.update({'placeholder': 'Soni'})
        self.fields['weight'].widget.attrs.update({'placeholder': 'Og\'irligi'})
        self.fields['price'].widget.attrs.update({'placeholder': 'Narxi(1 kg)'})


class BazarChiqimForm(ModelForm):
    payed_amount = forms.IntegerField(required=False, label='Mijozning To\'lagan summasi')
    weight_res = forms.CharField(label="Mahsulot og'irligi")
    weight = forms.FloatField(required=False, label='Mahsulot og\'irligi', widget=forms.HiddenInput(), initial=2.5)

    class Meta:
        model = IncomeSotuvchi
        fields = ['sotuvchi', 'product', 'source',  'quantity', 'weight_res', 'weight', 'price', 'payed_amount']

    def clean(self):
        cleaned_data = super().clean()
        try:
            weight = sum([int(i) for i in self.cleaned_data['weight_res'].split('+') if i])
        except ValueError:
            raise ValidationError('Og\'irligi to\'g\'ri kiriting')
        cleaned_data['weight'] = weight
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=True)
        print(type(instance), instance)
        if self.cleaned_data['payed_amount']:
            ExpenseSotuvchi.objects.create(
                income_sotuvchi=instance,
                amount=self.cleaned_data['payed_amount']
            )
        return instance



    def clean_weight(self):
        if 'product' not in self.cleaned_data or (
                'weight' not in self.cleaned_data) or 'weight_res' not in self.cleaned_data:
            raise ValidationError("Iltimos mahsulot va uning og'irligini kiriting")
        if self.cleaned_data['weight'] <= self.products[self.cleaned_data['product'].id]:
            return self.cleaned_data['product']
        else:
            raise ValidationError(
                "Sizda ushbu mahsulotdan {} kg mavjud".format(self.products[self.cleaned_data['product'].id]))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sotuvchi'].label = "Mijoz"
        self.fields['product'].label = "Mahsulot"
        self.fields['quantity'].label = "Mahsulot soni"
        self.fields['weight'].label = "Mahsulot og'irligi"
        self.fields['source'].label = "Qushxonadan yoki bozordan"

        # styling fields
        self.fields['sotuvchi'].widget.attrs.update({'class': 'form-control'})
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['weight_res'].widget.attrs.update({'class': 'form-control'})
        field = self.fields['weight']
        field.widget = field.hidden_widget()
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['payed_amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['source'].widget.attrs.update({'class': 'form-control'})
        # PLACEHOLDER
        self.fields['sotuvchi'].widget.attrs.update({'placeholder': 'Mijozni tanlang'})
        self.fields['product'].widget.attrs.update({'placeholder': 'Mahsulotni tanlang'})
        self.fields['quantity'].widget.attrs.update({'placeholder': 'Soni'})
        self.fields['weight_res'].widget.attrs.update({'placeholder': 'Og\'irligi(56+34+28+64)'})
        self.fields['price'].widget.attrs.update({'placeholder': 'Narxi(1 kg)'})
        self.fields['payed_amount'].widget.attrs.update({'placeholder': 'Mijozning to\'lovi'})
        # default values
        self.fields['weight'].initial = 0
        self.fields['quantity'].initial = 0

        # updating client and product querysets
        self.fields['sotuvchi'].queryset = self.fields['sotuvchi'].queryset.filter(role='client').order_by('full_name')
        products_income = BazarAllIncomeStock.objects.all().values('product', 'weight')
        products_expense = IncomeSotuvchi.objects.all().values('product', 'weight')
        product_income_res = []
        for i in products_income.distinct('product'):
            product_income_res.append({
                'product': i['product'],
                'weight': sum([j['weight'] for j in products_income.filter(product=i['product'])])
            })
        products_income = product_income_res
        products = {
            product['product']: product['weight'] - (products_expense.filter(product=product['product']).aggregate(
                Sum('weight'))['weight__sum'] or 0) for product in products_income
        }
        self.products = products
        self.fields['product'].queryset = Product.objects.filter(id__in=products.keys()).order_by('name')
