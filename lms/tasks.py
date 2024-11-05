from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config import settings
from lms.models import Course, Subscription


@shared_task
def send_email_to_subscribers(pk):
    """Функция отправки сообщения об обновлении курса подписчикам."""
    course = get_object_or_404(Course, pk=pk)
    subscribers = Subscription.objects.filter(course=course.pk)
    if subscribers:
        send_mail(
            subject=f"Обновление курса {course.name}",
            message=f"Обновлен курс - {course.name}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscriber.user.email for subscriber in subscribers],
        )
