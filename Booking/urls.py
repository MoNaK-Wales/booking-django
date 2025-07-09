from django.urls import path
from booking import views


app_name = 'main'

urlpatterns = [
    path('', views.home, name='locations'),
    path('location/<int:location_id>/', views.location_detail, name='location-info'),  
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('activate/<int:booking_id>/<str:token>/', views.activation, name='activation')
]
