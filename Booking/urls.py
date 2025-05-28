from django.urls import path
from Booking import views


app_name = 'Booking'

urlpatterns = [
    path('', views.home, name='home'),  
]
