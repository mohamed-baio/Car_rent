from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,JsonResponse
from django.utils import timezone
from .models import Customer,Booking,Vehicle
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.timezone import now,datetime
from django.views import View
from .forms import CustomerForm




def make_booking(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        customer_name = request.POST.get('customer_name')
        date_of_hire = request.POST.get('date_of_hire')
        return_date = request.POST.get('return_date')

        try:
            date_of_hire = datetime.datetime.strptime(date_of_hire, '%Y-%m-%da').date()
            return_date = datetime.datetime.strptime(return_date, '%Y-%m-%d').date()
        except ValueError:
          
            return render(request, 'Car_rent/make-booking.html', {'error': 'Invalid date format'})

       
        if return_date <= date_of_hire:
            return render(request, 'Car_rent/make-booking.html', {'error': 'Return date should be later than the date of hire'})

      
        customer, created = Customer.objects.get_or_create(name=customer_name)

    
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
        except Vehicle.DoesNotExist:
            return render(request, 'Car_rent/make-booking.html', {'error': 'Invalid vehicle'})

        
        existing_booking = Booking.objects.filter(vehicle=vehicle, date_of_hire__lte=return_date, return_date__gte=date_of_hire).first()
        if existing_booking:
            return render(request, 'Car_rent/make-booking.html', {'error': 'Vehicle is already booked for the specified period'})

      
        booking = Booking.objects.create(vehicle=vehicle, customer=customer, date_of_hire=date_of_hire, return_date=return_date)

      
        return redirect('booking_success')

    return render(request, 'Car_rent/make-booking.html')

    

def generate_invoice(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
   
    invoice_html = render_to_string("invoice.html", {"booking": booking})

   
    email = EmailMessage(
        subject="Invoice for your booking",
        body="Please find attached the invoice for your booking.",
        from_email="your_email@example.com",
        to=[booking.customer.email],  
    )
    email.attach(filename="invoice.pdf", content=invoice_html, mimetype="application/pdf")
    email.send()

    return HttpResponse("Invoice sent successfully!")


def check_availability(request):
    if request.method == 'POST':
        vehicle_type = request.POST.get('vehicle_type')
        desired_date = request.POST.get('desired_date')

        try:
            desired_date = datetime.datetime.strptime(desired_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'car_rent/check_availability.html', {'error': 'Invalid date format'})

   
        if vehicle_type not in ['small_car', 'family_car', 'van']:
            return render(request, 'car_rent/check_availability.html', {'error': 'Invalid vehicle type'})

     
        if desired_date < now().date():
            return render(request, 'car_rent/check_availability.html', {'error': 'Desired date should be in the future'})

     
        available_vehicles = Vehicle.objects.filter(type=vehicle_type)

    
        bookings = Booking.objects.filter(date_of_hire=desired_date)

        
        booked_vehicle_ids = bookings.values_list('vehicle__id', flat=True)
        available_vehicles = available_vehicles.exclude(id__in=booked_vehicle_ids)

        return render(request, 'car_rent/check_availability.html', {'available_vehicles': available_vehicles, 'desired_date': desired_date})

    return render(request, 'car_rental/check_availability.html')

def daily_report(request):
    today = datetime.today()
    bookings = Booking.objects.filter(date_of_hire=today)
    return render(request, 'car_rent/daily_report.html', {'bookings': bookings})




class CustomerDetailView(View):
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            data = {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                # Include other customer fields as needed
            }
            return JsonResponse(data)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
        

class CustomerUpdateView(View):
    def post(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            form = CustomerForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Customer updated successfully'})
            else:
                return JsonResponse({'error': 'Invalid data'}, status=400)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)    

def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'DELETE':
        customer.delete()
        return JsonResponse({'message': 'Customer deleted successfully'})

    return JsonResponse({'message': 'Invalid request method'}, status=405)            











