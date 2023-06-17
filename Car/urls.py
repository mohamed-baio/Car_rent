"""
URL configuration for Car project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from Car_rent import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('Car_rent/', include('Car_rent.urls', namespace='Car_rent')),
    path('customer/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('customer/<int:pk>/', views.CustomerUpdateView.as_view(), name='customer-update'),
    path('customers/<int:customer_id>/delete/', views.delete_customer, name='delete_customer'),
]
