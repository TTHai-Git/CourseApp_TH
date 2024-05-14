from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
import courses.pagination
from courses.models import Course, Category, Lesson, User, Tag, Comment, Like
from courses import serializers, pagination, perms

# Create your views here.


def index(request):
    return HttpResponse("CourseApp")


class CourseViewSet(viewsets.ViewSet, viewsets.generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    pagination_class = courses.pagination.CoursesPaginator

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

    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lessons(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)
        q = self.request.query_params.get('q')
        if q:
            lessons = lessons.filter(subject__icontains=q)

        return Response(serializers.LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = serializers.CategorySerializer
    pagination_class = courses.pagination.CategoriesPaginator

    @action(methods=['post'], detail=True)
    def hide_category(self, pk=None):
        category = Category.objetcts.get(pk=pk)
        try:
            category.active = False
            category.save()
        except category.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializers.CategorySerializer(category).data, status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class LessonViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer

    def get_permissions(self):
        if self.action in ['add_comment', 'like', 'add_tags']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return serializers.AuthenticatedLessonDetailsSerializer
        return self.serializer_class

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        lesson = self.get_object()
        try:
            comments = lesson.comment_set.select_related('user').order_by('-id')
            paginator = pagination.CommentPaginator()
            page = paginator.paginate_queryset(comments, request)
            if page is not None:
                serializer = serializers.CommentSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
        except lesson.DoesNotExist | KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='add-tags', detail=True)
    def add_tags(self, request, pk):
        lesson = self.get_object()
        try:
            tags = request.data.get('tags')

            for tag in tags.split(','):
                tag_name = tag.strip()
                t, created = Tag.objects.get_or_create(name=tag_name)
                lesson.tags.add(t)

            lesson.save()

        except lesson.DoesNotExist | KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.LessonSerializer(lesson).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path="add-comments", detail=True)
    def add_comment(self, request, pk):
        lesson = self.get_object()
        try:
            comment = lesson.comment_set.create(content=request.data.get('content'), user=request.user)
        except lesson.DoesNotExist | KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        lesson = self.get_object()
        try:
            li, created = Like.objects.get_or_create(lesson=lesson, user=request.user)
            if not created:
                li.active = not li.active
                li.save()
        except lesson.DoesNotExist | KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.AuthenticatedLessonDetailsSerializer(lesson).data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['get_current_user']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()
        return Response(serializers.UserSerializer(user).data)


class CommentViewSet(viewsets.ViewSet, generics.ListAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.filter(active=True)
    permissions_classes = [perms.CommentOwner]
    serializer_class = serializers.CommentSerializer

    # def destroy(self, request, *args, **kwargs):
    #     comment = self.get_object()
    #     if comment.user == request.user:
    #         comment.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(methods=['patch'], url_path='update_comment', detail=True)
    # def update_comment(self, request, pk):
    #     comment = self.get_object()
    #     if comment.user == request.user:
    #         comment.content = request.data.get('content')
    #         comment.save()
    #         return Response(serializers.CommentSerializer(comment).data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
