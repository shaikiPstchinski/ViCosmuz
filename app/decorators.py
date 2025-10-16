from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def astronomer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        if request.user.type != 'astronomer':
            messages.error(request, 'You must be an astronomer to access this page.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
