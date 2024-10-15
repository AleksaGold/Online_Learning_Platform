from rest_framework.routers import DefaultRouter

from lms.views import CourseViewSet

from lms.apps import LmsConfig

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename="courses")

urlpatterns = []

urlpatterns += router.urls
