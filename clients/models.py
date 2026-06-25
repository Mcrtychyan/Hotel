from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import BaseUserManager


class ClientManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Имя пользователя обязательно')
        client = self.model(username=username, **extra_fields)
        client.set_password(password)
        client.save(using=self._db)
        return client

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, password, **extra_fields)


class Client(models.Model):
    objects = ClientManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone', 'passport_number']

    username = models.CharField(max_length=150, unique=True, verbose_name="Логин")

    name = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Телефон")
    email = models.EmailField(unique=True, verbose_name="Email")
    birth_date = models.DateField(
        verbose_name="Дата рождения",
        null=True,
        blank=True
    )
    passport_number = models.CharField(max_length=20, unique=True, verbose_name="Номер паспорта")
    password = models.CharField(max_length=128, verbose_name="Хеш пароля")

    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Доступ в админку")
    is_superuser = models.BooleanField(default=False, verbose_name="Суперпользователь")

    def set_password(self, raw_password):
        self.password = make_password(raw_password)  # ИЗМЕНИЛ

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # ИЗМЕНИЛ

    def get_username(self):
        return self.username

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"