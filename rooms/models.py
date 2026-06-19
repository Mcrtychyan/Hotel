from django.db import models
from django.template.defaultfilters import slugify


class Room(models.Model):
    ROOM_TYPES = [
        ('standard', 'Стандарт'),
        ('superior', 'Полулюкс'),
        ('suite', 'Люкс'),
    ]

    STATUS_CHOICES = [
        ('available', 'Доступен'),
        ('occupied', 'Занят'),
        ('reserved', 'Забронирован'),
    ]
    room_number = models.CharField(max_length=10, unique=True, verbose_name="Номер комнаты")
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, verbose_name="Тип номера")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за день")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")
    status = models.CharField(max_length=20,default='available', choices=STATUS_CHOICES, verbose_name="Статус")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL")
    image = models.ImageField(upload_to='rooms/', blank=True, null=True, verbose_name="Фото номера")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"room-{self.room_number}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Комната {self.room_number} - {self.get_room_type_display()}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('rooms:detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"



