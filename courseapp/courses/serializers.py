from rest_framework.serializers import ModelSerializer
from courses.models import Course, Category


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'created_date', 'category']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
