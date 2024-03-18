from rest_framework.serializers import ModelSerializer
from courses.models import Course, Category, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
