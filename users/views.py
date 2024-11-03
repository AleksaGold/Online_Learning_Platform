from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.permissions import IsUserPermission
from users.serializers import (PaymentSerializer, UserSerializer,
                               UserShortcutSerializer)
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_session)


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

    def perform_create(self, serializer):
        """Переопределения метода для возможности оплаты курсов."""
        payment = serializer.save(user=self.request.user)
        product = create_stripe_product(payment.course)
        price = create_stripe_price(payment.payment_amount, product)
        session_id, session_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.payment_link = session_link
        payment.save()


class UserViewSet(ModelViewSet):
    """Вьюсет для работы с моделью User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        """Переопределение метода для вывода ограниченной информации по пользователям."""
        queryset = User.objects.all()
        serializer = UserShortcutSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Переопределение метода для вывода полной информации только по профилю пользователя."""
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        if self.request.user == user or self.request.user.is_superuser:
            serializer = UserSerializer(user)
        else:
            serializer = UserShortcutSerializer(user)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Сохраняет сериализованные данные при регистрации пользователя и хэширует пароль."""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        """Создает и возвращает список разрешений, требуемых для регистрации пользователя."""
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = (
                IsAuthenticated & IsUserPermission | IsAdminUser,
            )
        elif self.action in ["list", "retrieve"]:
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsAuthenticated & IsAdminUser,)
        return super().get_permissions()
