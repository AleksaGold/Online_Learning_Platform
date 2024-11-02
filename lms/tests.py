from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    """Тесты для модели Lesson."""

    def setUp(self):
        """Окружение для тестов."""
        self.user = User.objects.create(email="user@coo.coo")
        self.course = Course.objects.create(name="Тесты", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Тестирование",
            course=self.course,
            video_link="https://www.youtube.com/watch?v=YqedEln2Wis",
            owner=self.user,
        )
        self.lesson_without_owner = Lesson.objects.create(
            name="Тестирование прав доступа",
            course=self.course,
            video_link="https://www.youtube.com/watch?v=YqedEln2Wis",
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        """Тестирование создания нового урока с корректными данными."""
        url = reverse("lms:lessons_create")
        data = {
            "name": "Новый урок",
            "course": self.course.pk,
            "video_link": "https://www.youtube.com/watch?v=YqedEln2Wis",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 3)

    def test_lesson_create_without_youtube(self):
        """Тестирование создания нового урока с некорректной ссылкой на материалы."""
        url = reverse("lms:lessons_create")
        data = {
            "name": "Новый урок",
            "course": self.course.pk,
            "video_link": "https://www.youtube.ru/watch?v=YqedEln2Wis",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_retrieve(self):
        """Тестирование просмотра одного урока."""
        url = reverse("lms:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_update(self):
        """Тестирование обновления урока."""
        url = reverse("lms:lessons_update", args=(self.lesson.pk,))
        data = {"name": "Измененный урок"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Измененный урок")

    def test_lesson_delete(self):
        """Тестирование удаления урока."""
        url = reverse("lms:lessons_destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_lesson_list(self):
        """Тестирование просмотра списка уроков."""
        url = reverse("lms:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_link": self.lesson.video_link,
                    "name": self.lesson.name,
                    "description": None,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
        self.assertEqual(data["count"], 1)

    def test_lesson_retrieve_permissions(self):
        """Тестирование прав доступа к просмотру урока."""
        url = reverse("lms:lessons_retrieve", args=(self.lesson_without_owner.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_permissions(self):
        """Тестирование прав доступа к обновлению урока."""
        url = reverse("lms:lessons_update", args=(self.lesson_without_owner.pk,))
        data = {"name": "Измененный урок"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_permissions(self):
        """Тестирование прав доступа к удалению урока."""
        url = reverse("lms:lessons_destroy", args=(self.lesson_without_owner.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 2)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        """Окружение для тестов."""
        self.user = User.objects.create(email="user@coo.coo")
        self.course = Course.objects.create(name="Тесты", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        """Тестирование создания подписки."""
        url = reverse("lms:subscriptions")
        data = {"user": self.user.pk, "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(response.json(), {"message": "Подписка добавлена"})

    def test_subscription_delete(self):
        """Тестирование удаления подписки."""
        url = reverse("lms:subscriptions")
        self.subscription = Subscription.objects.create(
            user=self.user, course=self.course
        )
        data = {"user": self.user.pk, "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 0)
        self.assertEqual(response.json(), {"message": "Подписка удалена"})
