from django.urls import include, path
from rest_framework import routers

from courses import views

router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet, basename='course')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('lessons', views.LessonViewSet, basename='lesson')
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls))
]