from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.serializers import (CourseDetailSerializer, CourseSerializer,
                             LessonSerializer)
from users.permissions import IsModeratorPermission, IsOwnerPermission


class CourseViewSet(ModelViewSet):
    """Вьюсет для работы с моделью Course."""

    queryset = Course.objects.all()

    def get_serializer_class(self):
        """Возвращает класс сериализатора, который будет использоваться для обработки текущего запроса."""

        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_queryset(self):
        """Возвращает объекты, в зависимости от прав доступа."""
        if self.request.user.groups.filter(name="moderator"):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user.id)

    def get_permissions(self):
        """Возвращает список разрешений, требуемых для пользователей группы Moderator."""
        if self.action == "create":
            self.permission_classes = (IsAuthenticated & ~IsModeratorPermission,)
        elif self.action in ["update", "retrieve", "list"]:
            self.permission_classes = (
                IsAuthenticated & IsOwnerPermission | IsModeratorPermission,
            )
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated & IsOwnerPermission,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """Переопределение метода для автоматической привязки владельца к создаваемому объекту."""
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(CreateAPIView):
    """Представление для создания новых объектов модели Lesson."""

    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated & ~IsModeratorPermission,)

    def perform_create(self, serializer):
        """Переопределение метода для автоматической привязки владельца к создаваемому объекту."""
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """Представление для просмотра объектов модели Lesson."""

    def get_queryset(self):
        """Возвращает объекты, в зависимости от прав доступа."""
        if self.request.user.groups.filter(name="moderator"):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user.id)

    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated & IsModeratorPermission | IsOwnerPermission,)


class LessonRetrieveAPIView(RetrieveAPIView):
    """Представление для просмотра одного объекта модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated & IsModeratorPermission | IsOwnerPermission,)


class LessonUpdateAPIView(UpdateAPIView):
    """Представление для обновления объектов модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated & IsModeratorPermission | IsOwnerPermission,)


class LessonDestroyAPIView(DestroyAPIView):
    """Представление для удаления объектов модели Lesson."""

    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsOwnerPermission,)
