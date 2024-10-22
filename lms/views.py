from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.serializers import (CourseDetailSerializer, CourseSerializer,
                             LessonSerializer)
from users.permissions import IsModeratorPermission


class CourseViewSet(ModelViewSet):
    """Вьюсет для работы с моделью Course."""

    queryset = Course.objects.all()

    def get_serializer_class(self):
        """Возвращает класс сериализатора, который будет использоваться для обработки текущего запроса."""

        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        """Возвращает список разрешений, требуемых для пользователей группы Moderator."""
        if self.action in ["create", "destroy"]:
            self.permission_classes = (~IsModeratorPermission,)
        elif self.action in ["update", "retrieve", "list"]:
            self.permission_classes = (IsModeratorPermission,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """Представление для создания новых объектов модели Lesson."""

    permission_classes = (~IsModeratorPermission,)


class LessonListAPIView(ListAPIView):
    """Представление для просмотра объектов модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    """Представление для просмотра одного объекта модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    """Представление для обновления объектов модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    """Представление для удаления объектов модели Lesson."""

    queryset = Lesson.objects.all()
    permission_classes = (~IsModeratorPermission,)
