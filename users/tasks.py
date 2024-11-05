from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_active_users():
    """Фоновая задача, которая проверяет пользователей по дате последнего входа
    и блокирует пользователя, если он не заходил более 1 месяца"""
    today = timezone.now()
    active_users = User.objects.filter(is_active=True)
    for user in active_users:
        if user.last_login is None:
            if user.date_joined + timedelta(days=30) < today:
                user.is_active = False
                user.save()
        elif user.last_login + timedelta(days=30) < today:
            user.is_active = False
            user.save()
