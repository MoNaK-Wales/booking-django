from django.urls import path
from auth_users import views


app_name = 'auth'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('edit/', views.edit_profile, name='edit_profile'),
]