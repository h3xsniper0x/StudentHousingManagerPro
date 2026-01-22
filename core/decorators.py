from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser or request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return redirect('home') 
        return wrapper
    return decorator
