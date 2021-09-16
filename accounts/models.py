from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name= models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name

class Products(models.Model):
    CATEGORY=(
        ('indoor','indoor'),
        ('outdoor','outdoor')
    )
    name= models.CharField(max_length=100, null=True)
    price= models.FloatField(null=True)
    category= models.CharField(max_length=100, null=True,choices=CATEGORY)
    description= models.CharField(max_length=100, null=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)
    tags=models.ManyToManyField(Tag)
    def __str__(self):
        return self.name


class Order(models.Model):
    customers=models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    products=models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
    STATUS = (
        ('Pending', 'Pending'), 
        ('Out of Delivery', 'Out of Delivery'),
         ('Delivered', 'Delivered')
    )
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    status=models.CharField(max_length=100, null=True,choices=STATUS)
    def __str__(self):
        return self.products