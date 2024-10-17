from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class PaymentViewSet(ModelViewSet):
    """Вьюсет для работы с моделью Payment"""

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
    """Вьюсет для работы с моделью User"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
