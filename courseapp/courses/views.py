from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics
from courses.models import Course, Category
from courses.serializers import CourseSerializer, CategorySerializer


# Create your views here.
def index(request):
    return HttpResponse("CourseApp")


class CourseViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    permissions_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer
    permissions_classes = [permissions.IsAuthenticated]
