from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from lms.models import Course, Lesson

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


class Payment(models.Model):
    """Класс для описания модели Payment"""

    CASH = "cash"
    TRANSFER = "transfer"
    PAYMENT_METHOD = [
        (CASH, "Наличные"),
        (TRANSFER, "Банковский перевод"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Пользователь", **NULLABLE
    )
    payment_date = models.DateField(auto_now=False, verbose_name="Дата оплаты")

    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="Оплаченный курс", **NULLABLE
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.SET_NULL, verbose_name="Оплаченный урок", **NULLABLE
    )

    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD, verbose_name="Способ оплаты"
    )

    def __str__(self):
        return f"{self.course if self.course else self.lesson} : {self.user} "

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ("user",)
