from rest_framework import pagination


class CoursesPagination(pagination.PageNumberPagination):
    page_size = 5


class CategoriesPagination(pagination.PageNumberPagination):
    page_size = 5


class CommentPaginator(pagination.PageNumberPagination):
    page_size = 5
