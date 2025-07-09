from django.contrib import admin
from booking.models import BookingItem, Booking, Review

# Register your models here.
# admin.site.register(BookingItem)
# admin.site.register(Booking)

@admin.register(BookingItem)
class BookingItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'capacity', 'price', 'is_active', 'created_at')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_item', 'user', 'start_date', 'end_date', 'is_confirmed', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('place', 'rating', 'created_at')