from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import viewsets, permissions, generics, status, parsers
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

import courses.pagination
from courses.models import Course, Category, Lesson, User
from courses import serializers


# Create your views here.

def index(request):
    return HttpResponse("CourseApp")


class SecurityViewSet(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication, TokenAuthentication]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class CourseViewSet(viewsets.ViewSet, viewsets.generics.ListAPIView, SecurityViewSet):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    pagination_class = courses.pagination.CoursesPagination

    def get_queryset(self):
        queryset = self.queryset
        if self.action.__eq__('list'):
            sub = self.request.query_params.get('sub')

            if sub:
                queryset = queryset.filter(subject__icontains=sub)

            category_id = self.request.query_params.get('cate_id')
            if category_id:
                queryset = queryset.filter(category_id=category_id)
        return queryset

    # def list(self, request):
    #     courses = Course.objects.filter(active=True)
    #     serializer = CourseSerializer(courses, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk):
    #     try:
    #         course = Course.objects.get(pk=pk)
    #     except course.DoesNotExist:
    #         return Http404()
    #     return Response(CourseSerializer(course).data)
    #
    # def create(self, request):
    #     d = request.data
    #     c = Course.objects.create(subject=d['subject'],
    #                               category=d['category'],
    #                               tags=d['tags'])
    #     serializer = CourseSerializer(c)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         return [IsAuthenticated()]
    #     return [IsAdminUser()]

    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lessons(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)
        q = self.request.query_params.get('q')
        if q:
            lessons = lessons.filter(subject__icontains=q)

        return Response(serializers.LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView, SecurityViewSet):
    queryset = Category.objects.filter(active=True)
    serializer_class = serializers.CategorySerializer

    # permissions_classes = [permissions.IsAuthenticated]

    # def list(self, request):
    #     category = Category.objects.filter(active=True)
    #     serializer = CategorySerializer(category, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk):
    #     try:
    #         category = Category.objects.get(pk=pk)
    #     except category.DoesNotExist:
    #         return Http404()
    #     return Response(CategorySerializer(category).data)
    #
    # def create(self, request):
    #     d = request.data
    #     c = Category.objects.create(name=d['name'])
    #     serializer = CategorySerializer(c)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def hide_category(self, request, pk=None):
        try:
            category = Category.objetcts.get(pk=pk)
            category.active = False
            category.save()
        except Category.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.CategorySerializer(category)
        return Response(serializer.data, status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, SecurityViewSet):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, SecurityViewSet):
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAdminUser]
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]
