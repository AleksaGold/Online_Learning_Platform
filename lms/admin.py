from django.contrib import admin

from lms.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Course" в административной панели"""

    list_display = (
        "pk",
        "name",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Lesson" в административной панели"""

    list_display = ("pk", "name", "course")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Subscription" в административной панели"""

    list_display = ("pk", "user", "course")
