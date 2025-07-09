from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.urls import reverse
from booking.models import BookingItem, Booking
from config import settings

# Create your views here.
def home(request):
    return render(request, 'booking/locations.html', context={'locations': BookingItem.objects.all()})

def location_detail(request, location_id):
    if request.method == 'GET':
        try:
            location = BookingItem.objects.get(id=location_id)
            return render(request, 'booking/location-info.html', context={'location': location})
        except BookingItem.DoesNotExist:
            return redirect('booking:locations')
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'booking/location-info.html', context={'location': BookingItem.objects.get(id=location_id), 'error': "Ви повинні увійти в систему"})
        try:
            token = get_random_string(length=16)
            booking = Booking.objects.create(
                user=request.user,
                booking_item=BookingItem.objects.get(id=location_id),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                token=token,
            )

            url=f"{request.scheme}://{request.get_host()}" \
                f"{reverse('main:activation', args=[booking.pk, token])}"
            send_mail(
                subject='Бронювання локації',
                message=url,
                # message=f"Вітаємо, {request.user.username}! Ви успішно забронювали локацію {BookingItem.objects.get(id=location_id).title} з {request.POST.get('start_date')} по {request.POST.get('end_date')}.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email],
                fail_silently=False,
            )
            
            booking.save()
            return redirect('main:locations')
        except ValidationError as e:
            return render(request, 'booking/location-info.html', context={'location': BookingItem.objects.get(id=location_id), 'error': e.message})
        
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:locations')
    else:
        form = UserCreationForm()
    
    return render(request, 'booking/register.html', context={'form': form})

def login_user(request):
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
    
    return render(request, 'booking/login.html', context={'form': form})

def logout_user(request):
    logout(request)
    return redirect('main:locations')


def activation(request, booking_id, token):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.token == token:
        booking.is_confirmed = True
        booking.save()
    return redirect('main:locations')

#TODO: добавить имейл в регистрацию, добавить проверку через имейл