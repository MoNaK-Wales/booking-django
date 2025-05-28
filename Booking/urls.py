from django.urls import path
from Booking import views


app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),  
]
