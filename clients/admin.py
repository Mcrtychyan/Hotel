from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'surname', 'name', 'phone', 'email']
    list_display_links = ['id', 'surname']
    search_fields = ['surname', 'name', 'phone', 'email']
    list_filter = ['birth_date']
    fields = ['name', 'surname', 'middle_name', 'phone', 'email', 'birth_date', 'passport_number']