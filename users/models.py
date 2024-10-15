from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель User для хранения информации о пользователях веб-приложения"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="Аватар", **NULLABLE
    )
    token = models.CharField(max_length=100, verbose_name="Токен", **NULLABLE)
    phone_number = PhoneNumberField(verbose_name="Номер телефона", **NULLABLE)
    city = models.CharField(max_length=150, verbose_name="Страна", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Возвращает строковое представление объекта"""
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
