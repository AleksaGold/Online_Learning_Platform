from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class PaymentViewSet(ModelViewSet):
    """Вьюсет для работы с моделью Payment."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = (
        "payment_method",
        "course",
        "lesson",
    )
    ordering_fields = ("payment_date",)


class UserViewSet(ModelViewSet):
    """Вьюсет для работы с моделью User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Сохраняет сериализованные данные при регистрации пользователя и хэширует пароль."""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        """Создает и возвращает список разрешений, требуемых для регистрации пользователя."""
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
