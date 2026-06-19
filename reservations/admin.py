from django.contrib import admin
from .models import Reservation, Resident, Payment

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'room', 'check_in_date', 'departure_date', 'reservation_status']
    list_filter = ['reservation_status', 'check_in_date']
    search_fields = ['client__surname', 'client__name', 'room__room_number']
    date_hierarchy = 'check_in_date'

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ['reservation', 'client', 'check_in_time', 'check_out_time']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['reservation', 'amount', 'payment_date', 'payment_method', 'payment_status']
    list_filter = ['payment_method', 'payment_status']
