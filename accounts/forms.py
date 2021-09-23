from django import forms
from django.forms import ModelForm
from accounts.models import Customer,Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User



class CreateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name','email','phone','profile_pic']


class UpdateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class UpdateOrderForm(ModelForm):
    class Meta:
        model = Order
        fields=[ 'customers','products','status',]

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2']




