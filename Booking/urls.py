from django.urls import path
from booking import views


app_name = 'main'

urlpatterns = [
    path('', views.home, name='locations'),
    path('location/<int:location_id>/', views.location_detail, name='location-info'),  
]
