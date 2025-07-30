from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.urls import reverse
from booking.models import BookingItem, Booking
from config import settings

# Create your views here.
def home(request):
    return render(request, 'booking/home.html')

def locations(request):
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

            
            booking.save()
            return redirect('main:locations')
        except ValidationError as e:
            return render(request, 'booking/location-info.html', context={'location': BookingItem.objects.get(id=location_id), 'error': e.message})
        

def profile(request):
    if not request.user.is_authenticated:
        return redirect('auth:login')
    
    if request.method == 'POST':
        pass

    bookings = Booking.objects.filter(user=request.user).all()
    return render(request, 'booking/profile.html', context={'bookings': bookings})

def activation(request, booking_id, token):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.token == token:
        booking.is_confirmed = True
        booking.save()
    return redirect('main:locations')

def email_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)


    url=f"{request.scheme}://{request.get_host()}" \
                f"{reverse('main:activation', args=[booking.pk, booking.token])}"
    send_mail(
        subject='Бронювання локації',
        message=f"Вітаємо, {request.user.username}! Ви забронювали локацію {booking.title} з {booking.start_date} по {booking.end_date}.\n"\
                f"Щоб підтвердити бронювання, перейдіть за посиланням: {url}",
        # message=url,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
        fail_silently=False,
    )

#TODO: добавить имейл в регистрацию, добавить проверку через имейл, добавить подтверждение существующего бронирования