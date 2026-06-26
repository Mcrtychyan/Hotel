from django.contrib import admin
from .models import Client
# pip install -r requirements.txt - чтобы на другом компе все норм было https://www.lightgalleryjs.com/
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'surname', 'name', 'phone', 'email']
    list_display_links = ['id', 'surname']
    search_fields = ['surname', 'name', 'phone', 'email']
    list_filter = ['birth_date']
    fields = ['name', 'surname', 'middle_name', 'phone', 'email', 'birth_date', 'passport_number']

    def log_addition(self, request, object, message):
        return

    def log_change(self, request, object, message):
        return

    def log_deletion(self, request, object, object_repr):
        return