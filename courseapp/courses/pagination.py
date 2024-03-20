from rest_framework import pagination


class CoursesPagination(pagination.PageNumberPagination):
    page_size = 2
