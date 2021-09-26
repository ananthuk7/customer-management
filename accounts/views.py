from accounts.models import Order, Customer, Products
from django.shortcuts import redirect, render
from accounts.forms import CreateCustomerForm, UpdateCustomerForm, UpdateOrderForm, RegistrationForm
from django.forms.models import inlineformset_factory
from accounts.filter import OrderFilter
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .decorators import user_login_page,allowed_user,admin_only
from django.contrib.auth.models import Group
# Create your views here.


@login_required(login_url='login')
@admin_only
def home(request, *args, **kwargs):
    orders = Order.objects.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    customers = Customer.objects.all()
    context = {'orders': orders, 'customers': customers, 'orders_delivered': orders_delivered,
               'orders_pending': orders_pending, 'total_orders': total_orders}
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])
def products(request, *args, **kwargs):
    products = Products.objects.all()
    context = {'products': products}
    return render(request, 'product.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])
def customer(request, id, *args, **kwargs):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    total_orders = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders,
               'total_orders': total_orders, 'myFilter': myFilter}
    return render(request, 'customer.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])
def create_customer(request):
    form = CreateCustomerForm()
    context = {'form': form}
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            
            
           
            messages.success(request, 'account was created successfully'+ username)
            return redirect('home')
        else:
            return render(request, 'customercreate.html', context)
    return render(request, 'customercreate.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])
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


@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])
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


@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])
def order_remove(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    else:
        return render(request, 'removeorder.html', {'order': order})


@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])
def order_create(request, id):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('products', 'status'), extra=10)
    customer = Customer.objects.get(id=id)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context = {'formset': formset}
    return render(request, 'ordercreate.html', context)

@user_login_page
def register(request):

    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['username']
            messages.success(request, 'account was created for ' + user)
            return redirect('login')
    return render(request, 'registration.html', {'form': form})

@user_login_page
def loginpage(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'incorrect username or password')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_user(allowed_role=['customer'])
def user_home_page(request):
   
    orders=request.user.customer.order_set.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'orders_delivered': orders_delivered,
               'orders_pending': orders_pending, 'total_orders': total_orders}
    return render(request, 'user.html', context)

@login_required(login_url='login')
@allowed_user(allowed_role=['customer'])
def customer_settings(request):
    customer= request.user.customer
    form= CreateCustomerForm(instance=customer,files=request.FILES)
    context={'form':form}
    if request.method == 'POST':
        form=CreateCustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            context={'form':form}
            return render(request, 'usersettings.html',context)

    return render(request, 'usersettings.html',context)
    