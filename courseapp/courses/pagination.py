from rest_framework import pagination

from courses.models import Category


class CoursesPagination(pagination.PageNumberPagination):
    page_size = 22


class CategoriesPagination(pagination.PageNumberPagination):
    page_size = 4
