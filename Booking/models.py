from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.
class BookingItem(models.Model):
    title = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["capacity"]
        verbose_name = "Booking Item"
        verbose_name_plural = "Booking Items"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    booking_item = models.ForeignKey(BookingItem, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_confirmed = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.start_date >= self.end_date:
            raise ValidationError(_("Дата початку не може бути пізніше дати закінчення"))

        if (
            Booking.objects.filter(booking_item=self.booking_item).exclude(id=self.id)
            .filter(
                models.Q(start_date__lte=self.start_date)
                & models.Q(end_date__gte=self.start_date)
            )
            .exists()
        ):
            raise ValidationError(_(f"Ці дати вже зайняті для {self.booking_item.title}"))
        
        if self.booking_item.is_active is False:
            raise ValidationError(_("Цей об'єкт бронювання неактивний"))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.user.username} in {self.booking_item}"

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"


class Review(models.Model):
    place = models.ForeignKey(BookingItem, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.place}"

# TODO: сделать страничку сайта, которая будет отображать все локации существующие