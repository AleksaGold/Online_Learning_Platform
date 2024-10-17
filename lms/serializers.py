from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """Сериализатор для модели Course"""

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """Сериализатор для поля вывода количества уроков Курса"""
    count_lessons = SerializerMethodField()

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("id", "name", "description", "preview", "count_lessons",)


class LessonSerializer(ModelSerializer):
    """Сериализатор для модели Lesson"""

    class Meta:
        model = Lesson
        fields = "__all__"
