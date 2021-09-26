from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.products, name='products'),
    path('customer/<int:id>', views.customer, name='customer'),
    path('customer/create', views.create_customer, name="createcustomer"),
    path('customer/change/<int:id>', views.update_customer, name="updatecustomer"),
    path('order/change/<int:id>', views.order_update, name="updateorder"),
    path('order/delete/<int:id>', views.order_remove, name="removeorder"),
    path('order/create/<int:id>', views.order_create, name="createorder"),
    path('customer/login', views.loginpage, name="login"),
    path('customer/register', views.register, name="register"),
    path('customer/logout', views.user_logout, name="logout"),
    path('user', views.user_home_page, name="user-page"),
    path('user/settings', views.customer_settings, name="custsettings"),

]
