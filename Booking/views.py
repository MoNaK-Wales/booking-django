from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime as dt
import json
from booking.models import BookingItem, Booking
from config import settings

# Create your views here.
def home(request):
    return render(request, 'booking/home.html')

def locations(request):
    return render(request, 'booking/locations.html', context={'locations': BookingItem.objects.all()})

def location_detail(request, location_id):
    try:
        location = BookingItem.objects.get(id=location_id)
        bookings = location.bookings.all()
        disable_intervals = []
        for booking in bookings:
            start = booking.start_date.strftime("%Y-%m-%d")
            end = booking.end_date.strftime("%Y-%m-%d")
            disable_intervals.append({"from": start, "to": end})
        disable_intervals = json.dumps(disable_intervals, cls=DjangoJSONEncoder)
        context = {
            'location': location,
            'disable': disable_intervals,
        }
    except BookingItem.DoesNotExist:
        return redirect('booking:locations')
    
    if request.method == 'GET':
        return render(request, 'booking/location-info.html', context=context)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            context['error'] = "Будь ласка, увійдіть у свій акаунт, щоб забронювати локацію."
            return render(request, 'booking/location-info.html', context=context)
        elif request.POST.get('date') == '': # TODO: после возврата обычный календарь
            context['error'] = "Будь ласка, виберіть дати для бронювання."
            return render(request, 'booking/location-info.html', context=context)
        
        try:
            date_range = request.POST.get('date')
            start_date, end_date = date_range.split(' to ')
            start_date = dt.strptime(start_date, '%d.%m.%Y').date()
            end_date = dt.strptime(end_date, '%d.%m.%Y').date()

            token = get_random_string(length=16)
            booking = Booking.objects.create(
                user=request.user,
                booking_item=BookingItem.objects.get(id=location_id),
                start_date=start_date,
                end_date=end_date,
                token=token,
            )
            email_confirmation(request, booking.id)

            return redirect('main:locations')
        except ValidationError as e:
            return render(request, 'booking/location-info.html', context={'location': BookingItem.objects.get(id=location_id), 'error': e.message})
        

def profile(request):
    if not request.user.is_authenticated:
        return redirect('auth:login')
    
    if request.method == 'POST':
        action = request.POST.get("action")
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)

        if action == 'delete':
            booking.delete()
        elif action == 'confirm':
            new_token = get_random_string(length=16)
            booking.token = new_token
            booking.save()
            email_confirmation(request, booking.id)
        
        return redirect('main:profile')

    bookings = Booking.objects.filter(user=request.user).all()
    return render(request, 'booking/profile.html', context={'bookings': bookings})

def activation(request, booking_id, token):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.token == token:
        booking.is_confirmed = True
        booking.save()
    return redirect('main:profile')

def email_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)


    url=f"{request.scheme}://{request.get_host()}" \
                f"{reverse('main:activation', args=[booking.pk, booking.token])}"
    send_mail(
        subject='Бронювання локації',
        message=f"Вітаємо, {request.user.username}! Ви забронювали локацію {booking.booking_item.title} з {booking.start_date} по {booking.end_date}.\n"\
                f"Щоб підтвердити бронювання, перейдіть за посиланням: {url}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
        fail_silently=False,
    )

#TODO: добавить имейл в регистрацию, добавить проверку через имейл, добавить подтверждение существующего бронирования