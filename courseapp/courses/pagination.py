from rest_framework import pagination


class CoursesPaginator(pagination.PageNumberPagination):
    page_size = 5


class CategoriesPaginator(pagination.PageNumberPagination):
    page_size = 5


class CommentPaginator(pagination.PageNumberPagination):
    page_size = 5
