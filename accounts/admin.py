from django.contrib import admin
from accounts.models import Customer,Order,Products,Tag

# Register your models here.
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Products)
admin.site.register(Tag)