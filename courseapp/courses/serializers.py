from rest_framework import serializers
from courses.models import Course, Category, Lesson, Tag, User, Comment


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = instance.image.url
        return rep


class CourseSerializer(ItemSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'created_date', 'updated_date', 'active', 'image', 'category']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializer(ItemSerializer):
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'created_date', 'image', 'updated_date', 'tags', 'content']


class LessonDetailsSerializer(LessonSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['tags']


class AuthenticatedLessonDetailsSerializer(LessonDetailsSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, lesson):
        return lesson.like_set.filter(active=True).exists()

    class Meta:
        model = LessonDetailsSerializer.Meta.model
        fields = LessonDetailsSerializer.Meta.fields + ['liked']


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data["password"])
        user.save()

        return user

    def update(self, instance, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data["password"])
        user.set_avatar(data["avatar"])
        user.save()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['avatar'] = instance.avatar.url

        return rep


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'avatar']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['avatar'] = instance.avatar.url
        return rep


class CommentSerializer(serializers.ModelSerializer):
    user = UserCommentSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date', 'user']
