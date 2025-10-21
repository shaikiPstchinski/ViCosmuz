from django.contrib import messages
from django.shortcuts import redirect

def astronomerRequired(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            messages.error(request, 'Você deve estar logado para acessar a página.')
            return redirect('login')

        if (user.type in ['astronomer'] and user.verified) or (user.is_staff or user.is_superuser):
            return view_func(request, *args, **kwargs)
        
        messages.error(request, 'Você deve ser um astrônomo para acessar a página.')
        return redirect('home')
    
    return wrapper
