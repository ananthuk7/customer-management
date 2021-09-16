from django.forms.models import inlineformset_factory
from accounts.models import Order, Customer, Products
from django.shortcuts import redirect, render
from accounts.forms import CreateCustomerForm, UpdateCustomerForm, UpdateOrderForm
from django.forms.models import inlineformset_factory

# Create your views here.


def home(request, *args, **kwargs):
    orders = Order.objects.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    customers = Customer.objects.all()
    context = {'orders': orders, 'customers': customers, 'orders_delivered': orders_delivered,
               'orders_pending': orders_pending, 'total_orders': total_orders}
    return render(request, 'dashboard.html', context)


def products(request, *args, **kwargs):
    products = Products.objects.all()
    context = {'products': products}
    return render(request, 'product.html', context)


def customer(request, id, *args, **kwargs):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    total_orders = orders.count()
    context = {'customer': customer, 'orders': orders,
               'total_orders': total_orders}
    return render(request, 'customer.html', context)


def create_customer(request):
    form = CreateCustomerForm()
    context = {'form': form}
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'customercreate.html', context)
    return render(request, 'customercreate.html', context)


def update_customer(request, id):
    customer = Customer.objects.get(id=id)
    form = UpdateCustomerForm(instance=customer)
    context = {'form': form}
    if request.method == 'POST':
        form = UpdateCustomerForm(request.POST, instance=customer)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'updatecustomer.html', context)
    return render(request, 'updatecustomer.html', context)


def order_update(request, id):
    order = Order.objects.get(id=id)
    form = UpdateOrderForm(instance=order)
    context = {'form': form}
    if request.method == 'POST':
        form = UpdateOrderForm(request.POST, instance=order)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'orderupdate.html', context)
    return render(request, 'orderupdate.html', context)


def order_remove(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    else:
        return render(request, 'removeorder.html', {'order': order})


def order_create(request, id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('products', 'status'),extra=10)
    customer = Customer.objects.get(id=id)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context = {'formset': formset}
    return render(request, 'ordercreate.html', context)
