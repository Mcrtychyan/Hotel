from django.contrib import admin
from django import forms
from django.utils.html import format_html
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