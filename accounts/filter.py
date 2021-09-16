import django_filters
from accounts.models import Order
from django_filters import DateFilter


class OrderFilter(django_filters.FilterSet):
    # start_date = django_filters.DateFilter(field_name='date_created',lookup_expr='lte')
    # end_date=django_filters.DateFilter(field_name='date_created',lookup_expr='gte')
    class Meta:
        model = Order
        fields ='__all__'
        exclude =['customers','date_created']