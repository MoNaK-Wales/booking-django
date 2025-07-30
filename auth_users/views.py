from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('main:locations')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:locations')
    else:
        form = CustomUserCreationForm()

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


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect("auth:login")

    user = get_user_model().objects.get(id=request.user.id)

    if request.method == "POST":
        form = ProfileUpdateForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль оновлено успішно.")
            return redirect("main:profile")
        else:
            messages.error(request, "Неправильні дані профілю.")
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, "auth_users/edit.html", context={"form": form})
