from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"{self.name} - {self.price} руб."

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class ServiceOrder(models.Model):
    reservation = models.ForeignKey(
        'reservations.Reservation',  # ← строка
        on_delete=models.CASCADE,
        related_name='service_orders',
        verbose_name="Бронирование"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Услуга"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")

    def __str__(self):
        return f"Заказ #{self.id} - {self.service.name} x{self.quantity}"

    class Meta:
        verbose_name = "Заказ услуги"
        verbose_name_plural = "Заказы услуг"