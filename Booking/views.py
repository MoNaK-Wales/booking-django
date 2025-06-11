from django.shortcuts import render, redirect
from booking.models import BookingItem

# Create your views here.
def home(request):
    return render(request, 'booking/locations.html', context={'locations': BookingItem.objects.all()})

def location_detail(request, location_id):
    try:
        location = BookingItem.objects.get(id=location_id)
        return render(request, 'booking/location-info.html', context={'location': location})
    except BookingItem.DoesNotExist:
        return redirect('booking:locations')