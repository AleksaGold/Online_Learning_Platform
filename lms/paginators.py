from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Кастомная реализация пагинации."""

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100
