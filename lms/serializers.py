from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_lesson_video_link


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Lesson."""

    video_link = serializers.URLField(validators=[validate_lesson_video_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Course."""

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для одного объекта Course."""

    count_lessons = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    subscribers = serializers.SerializerMethodField(read_only=True)

    def get_count_lessons(self, course):
        """Возвращает количество уроков курса."""
        return Lesson.objects.filter(course=course).count()

    def get_subscribers(self, course):
        """Возвращает подписчиков курса."""
        user = self.context["request"].user
        return Subscription.objects.filter(user=user).filter(course=course).exists()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "preview",
            "count_lessons",
            "lessons",
            "owner",
            "subscribers",
        )
