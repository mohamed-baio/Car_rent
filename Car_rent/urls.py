from django.urls import path 
from . import views
app_name = 'Car_rent'

urlpatterns = [
    path('make-booking/', views.make_booking, name='make-booking'),
    path('check-availability/', views.check_availability, name='check_availability'),
    path('daily-report/', views.daily_report, name='daily_report'),
]