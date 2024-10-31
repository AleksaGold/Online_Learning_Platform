from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import (CourseViewSet, LessonCreateAPIView,
                       LessonDestroyAPIView, LessonListAPIView,
                       LessonRetrieveAPIView, LessonUpdateAPIView, SubscriptionAPIView)

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path(
        "lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lessons_update"
    ),
    path(
        "lessons/destroy/<int:pk>/",
        LessonDestroyAPIView.as_view(),
        name="lessons_destroy",
    ),
    path(
        "lessons/retrieve/<int:pk>/",
        LessonRetrieveAPIView.as_view(),
        name="lessons_retrieve",
    ),
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscriptions"),
]

urlpatterns += router.urls
