from django.forms import ModelForm
from .models import IncomeBazarOther


class BozorBozorIncomeForm(ModelForm):
    class Meta:
        model = IncomeBazarOther
        fields = '__all__'
