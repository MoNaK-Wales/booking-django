from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Room №{self.number}"
    
    class Meta:
        ordering = ['number']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
    

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} in {self.room}"
    
    class Meta:
        ordering = ['start_time']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'