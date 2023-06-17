from django.contrib import admin
from .models import Customer,Vehicle,Booking,Invoice,ConfirmationLetter 

admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(Booking)
admin.site.register(Invoice)
admin.site.register(ConfirmationLetter)