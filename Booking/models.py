from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BookingItem(models.Model):
    title = models.CharField(max_length=100, unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['capacity']
        verbose_name = 'Booking Item'
        verbose_name_plural = 'Booking Items'
    

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booking_item = models.ForeignKey(BookingItem, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} in {self.booking_item}"
    
    class Meta:
        ordering = ['start_time']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'