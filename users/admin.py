from django.contrib import admin

from users.models import Payment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "User" в административной панели"""

    list_display = (
        "pk",
        "email",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Payment" в административной панели"""

    list_display = (
        "id",
        "user",
        "course",
        "lesson",
    )
