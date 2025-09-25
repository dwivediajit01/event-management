from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

def role_required(role, redirect_url='event_list'):
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name=role).exists():
                return view_func(request, *args, **kwargs)
            messages.error(request, f"You need to be a {role} to access this page.")
            return redirect(redirect_url)
        return wrapper   
    return decorator
