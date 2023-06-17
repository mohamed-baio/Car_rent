from django.db import models
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    CATEGORY_CHOICES = (
        ('small', 'Small Car'),
        ('family', 'Family Car'),
        ('van', 'Van'),
    )

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    

    def __str__(self):
        return f"{self.get_category_display()} - {self.id}"


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    hire_date = models.DateField()
    return_date = models.DateField()

    def clean(self):
        if (self.return_date - self.hire_date).days > 7:
            raise ValidationError("A booking cannot exceed one week.")


    def __str__(self):
        return f"Booking {self.id} - {self.customer} - {self.vehicle}"


class Invoice(models.Model):
    booking = models.ManyToManyField(Booking)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Invoice {self.id} - {self.booking}"


class ConfirmationLetter(models.Model):
    booking = models.ManyToManyField(Booking)

    def __str__(self):
        return f"Confirmation Letter {self.id} - {self.booking}"
    
    

