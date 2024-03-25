from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, status, parsers
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

import courses.pagination
from courses.models import Course, Category, Lesson, User, Tag
from courses import serializers


# Create your views here.

def index(request):
    return HttpResponse("CourseApp")


class SecurityViewSet(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    # authentication_classes = [BasicAuthentication, TokenAuthentication]

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

        return Response(serializers.CategorySerializer(category).data, status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, SecurityViewSet ):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.filter(active=True)
        return Response(serializers.CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='add-tags', detail=True)
    def add_tags(self, request, pk):
        try:
            lesson = self.get_object()
            tags = request.data.get('tags')

            for tag in tags.split(','):
                tag_name = tag.strip()
                t, created = Tag.objects.get_or_create(name=tag_name)
                lesson.tags.add(t)

            lesson.save()
        except Lesson.DoesNotExist | KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.LessonSerializer(lesson).data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, SecurityViewSet, generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAdminUser]
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    @action(methods=['list'], url_path='user', detail=True)
    def get_details(self, request, pk):
        user = self.get_object()
        return Response(serializers.UserSerializer(user).data, status=status.HTTP_200_OK)
