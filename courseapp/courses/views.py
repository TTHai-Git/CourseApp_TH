from django.http import HttpResponse, Http404
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import viewsets, permissions, generics, status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Category, Lesson
from courses.serializers import CourseSerializer, CategorySerializer, LessonSerializer


# Create your views here.

def index(request):
    return HttpResponse("CourseApp")


class CourseViewSet(viewsets.ViewSet):
    # queryset = Course.objects.filter(active=True)
    # serializer_class = CourseSerializer
    # permissions_classes = [permissions.IsAuthenticated]

    def list(self, request):
        courses = Course.objects.filter(active=True)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except course.DoesNotExist:
            return Http404()
        return Response(CourseSerializer(course).data)

    def create(self, request):
        d = request.data
        c = Course.objects.create(subject=d['subject'],
                                  category=d['category'],
                                  tags=d['tags'])
        serializer = CourseSerializer(c)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class CategoryViewSet(viewsets.ViewSet, viewsets.ModelViewSet):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer
    permissions_classes = [permissions.IsAuthenticated]

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

        serializer = CategorySerializer(category)
        return Response(serializer.data, status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class UserView(APIView):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        pass


schema_view = get_schema_view(
    openapi.Info(
        title="Course API",
        default_version='v1',
        description="APIs for CourseApp",
        contact=openapi.Contact(email="2151050112hai@ou.edu.vn"),
        license=openapi.License(name="Trịnh Thanh Hải@2024"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
