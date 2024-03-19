from rest_framework.serializers import ModelSerializer
from courses.models import Course, Category, Lesson, Tag, User


class ItemSerializer(ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['iamge'] = instance.image.url
        return rep


class CourseSerializer(ItemSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializer(ItemSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'created_date']


class LessonDetailsSerializer(LessonSerializer):
    tag = TagSerializer(many=True)

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content', 'image', 'course', 'tags']


class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        # import pdb
        # pdb.set_trace()
        user.set_password(user["password"])
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
