from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('main:locations')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:locations')
    else:
        form = UserCreationForm()
    
    return render(request, 'auth_users/register.html', context={'form': form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('main:locations')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:locations')
            else:
                messages.error(request, "Неправильне ім'я користувача або пароль")
    else:
        form = AuthenticationForm()
    
    return render(request, 'auth_users/login.html', context={'form': form})

def logout_user(request):
    if not request.user.is_authenticated:
        return redirect('auth:login')
    
    logout(request)
    return redirect('main:home')