from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.utils.text import slugify
from image_uploader_widget.widgets import ImageUploaderWidget
from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        widgets = {
            'image': ImageUploaderWidget(
                attrs={
                    'drop_text': 'Drop your image here or click to select one...',
                    'label': 'Изображение товара:',
                    'help_text': 'Загрузите фото товара (рекомендуемый размер: 300x300 пикселей)',
                }
            ),
        }


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    form = RoomForm
    list_display = ['room_number', 'room_type', 'price_per_day', 'capacity', 'status', 'image_preview']
    list_editable = ['status']
    list_filter = ['room_type', 'status']
    search_fields = ['room_number']
    readonly_fields = ['image_preview']

    prepopulated_fields = {'slug': ('room_number',)}

    fieldsets = (
        ('Основная информация', {
            'fields': ('room_number', 'room_type', 'price_per_day', 'capacity', 'status')
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview'),
            'description': 'Загрузите изображение товара (рекомендуемый размер: 300x300 пикселей)',
        }),
        ('Дополнительно', {
            'fields': ('slug',),
            'classes': ('collapse',),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="150" height="150" style="object-fit: cover; border-radius: 10px; border: 2px solid #d4af37;" />',
                obj.image.url
            )
        return 'Нет фото'

    image_preview.short_description = 'Превью'

    # ОТКЛЮЧАЕМ ЗАПИСЬ В ЛОГИ АДМИНКИ (ГЛАВНОЕ!)
    def log_addition(self, request, object, message):
        return

    def log_change(self, request, object, message):
        return

    def log_deletion(self, request, object, object_repr):
        return

    # Автоматически создаем slug при сохранении (на случай, если prepopulated_fields не сработает)
    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.room_number)
        super().save_model(request, obj, form, change)