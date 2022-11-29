import django_filters

from app.models import ExpenseClient


class ExpenseFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = ExpenseClient
        fields = ['date', 'category', 'amount']
