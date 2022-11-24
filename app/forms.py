from django.forms import ModelForm
from .models import IncomeBazarOther


class BozorBozorIncomeForm(ModelForm):
    class Meta:
        model = IncomeBazarOther
        fields = ['client', 'product', 'quantity', 'weight', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].label = 'Mijoz'
        self.fields['product'].label = 'Mahsulot'
        self.fields['quantity'].label = 'Soni'
        self.fields['weight'].label = "Og'irligi"
        self.fields['price'].label = 'Narxi(1 kg)'

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

