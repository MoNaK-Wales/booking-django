from django.urls import path
from booking import views


app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('locations/', views.locations, name='locations'),
    path('location/<int:location_id>/', views.location_detail, name='location-info'),  
    path('profile/', views.profile, name='profile'),
    path('activate/<int:booking_id>/<str:token>/', views.activation, name='activation')
]
