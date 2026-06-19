from django.db import models


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждена'),
        ('checked_in', 'Заселён'),
        ('checked_out', 'Выселен'),
        ('cancelled', 'Отменена'),
    ]

    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='reservations',
                               verbose_name="Клиент")
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='reservations', verbose_name="Номер")
    check_in_date = models.DateField(verbose_name="Дата заезда")
    departure_date = models.DateField(verbose_name="Дата выезда")
    reservation_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending',
                                          verbose_name="Статус бронирования")

    def __str__(self):
        return f"Бронь #{self.id}"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"


class Resident(models.Model):
    reservation = models.ForeignKey('reservations.Reservation', on_delete=models.CASCADE, related_name='residents',
                                    verbose_name="Бронирование")
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='residencies',
                               verbose_name="Клиент")
    check_in_time = models.DateTimeField(verbose_name="Время заезда")
    check_out_time = models.DateTimeField(blank=True, null=True, verbose_name="Время выезда")

    def __str__(self):
        return f"Проживание"

    class Meta:
        verbose_name = "Проживающий"
        verbose_name_plural = "Проживающие"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('bank', 'Банковский перевод'),
        ('online', 'Онлайн'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Ожидает'),
        ('completed', 'Завершён'),
        ('failed', 'Неудачно'),
        ('refunded', 'Возвращён'),
    ]

    reservation = models.ForeignKey('reservations.Reservation', on_delete=models.CASCADE, related_name='payments',
                                    verbose_name="Бронирование")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата платежа")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name="Метод оплаты")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending',
                                      verbose_name="Статус оплаты")

    def __str__(self):
        return f"Платёж #{self.id} - {self.amount} руб."

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"