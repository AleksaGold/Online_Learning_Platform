from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription
from lms.paginators import CustomPagination
from lms.serializers import (CourseDetailSerializer, CourseSerializer,
                             LessonSerializer)
from users.permissions import IsModeratorPermission, IsOwnerPermission


class CourseViewSet(ModelViewSet):
    """Вьюсет для работы с моделью Course."""

    queryset = Course.objects.all()
    pagination_class = CustomPagination

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
    pagination_class = CustomPagination


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


class SubscriptionAPIView(APIView):
    """Представление для управления подписками пользователей."""

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
        return Response({"message": message})
