from django.shortcuts import redirect
from django.http import HttpResponse


def user_login_page(func):
    def wrapper(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return(func(request,*args, **kwargs))
    return wrapper

def allowed_user(allowed_role=[]):
    def decorator(func):
        def wrapper(request,*args, **kwargs):
            group=None
            if request.user.groups.exists():
                group= request.user.groups.all()[0].name
            if group in allowed_role:
                return(func(request,*args,**kwargs))
            else:
                return HttpResponse('un authorised user')
        return wrapper
    return decorator

def admin_only(func):
    def wrapper(request,*args, **kwargs):
        group=None
        if request.user.groups.exists():
            group= request.user.groups.all()[0].name
        if group == 'admin':
            return(func(request,*args,**kwargs))
        if group == 'customer':
            return redirect('user-page')
    return wrapper
