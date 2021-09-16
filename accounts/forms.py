from django import forms
from django.forms import ModelForm
from accounts.models import Customer,Order



class CreateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class UpdateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class UpdateOrderForm(ModelForm):
    class Meta:
        model = Order
        fields=[ 'customers','products','status',]



