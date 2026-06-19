from django.contrib import admin
from .models import Service, ServiceOrder

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']

@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'reservation', 'service', 'quantity', 'order_date']
    list_filter = ['order_date']