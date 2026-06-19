from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Client(models.Model):
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']
    name = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, verbose_name="Отчество")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Телефон")
    email = models.EmailField(unique=True, verbose_name="Email")
    birth_date = models.DateField(verbose_name="Дата рождения")
    passport_number = models.CharField(max_length=20, unique=True, verbose_name="Номер паспорта")
    password_hash = models.CharField(max_length=128, verbose_name="Хеш пароля")

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def get_username(self):
        return self.phone

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def has_perm(self, perm, obj=None):
        return False

    def has_module_perms(self, app_label):
        return False

    def __str__(self):
        return f"{self.surname} {self.name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"