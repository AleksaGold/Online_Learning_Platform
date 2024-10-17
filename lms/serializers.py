from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Сериализатор для модели Lesson"""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """Сериализатор для модели Course"""

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """Сериализатор для одного объекта Course"""

    count_lessons = SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_lessons(self, course):
        """Возвращает количество уроков курса"""
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "preview",
            "count_lessons",
            "lessons",
        )
