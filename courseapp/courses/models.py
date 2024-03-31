from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


# from cloudinary.models import CloudinaryField


class User(AbstractUser):
    avatar = CloudinaryField(null=True)

    def __str__(self):
        return f'{self.id} - {self.last_name}  {self.first_name} - {self.username}'


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.id} - {self.name} - {self.created_date} - {self.updated_date}'


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class ItemBase(BaseModel):
    tags = models.ManyToManyField(Tag)

    class Meta:
        abstract = True


class Course(ItemBase):
    subject = models.CharField(max_length=255)
    description = RichTextField(null=True)
    # image = models.ImageField(upload_to='courses/%Y/%m/', null=True, blank=True)
    image = CloudinaryField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.subject} - {self.created_date} - {self.updated_date} - {self.category}'


class Lesson(ItemBase):
    subject = models.CharField(max_length=255)
    content = RichTextField()
    # image = models.ImageField(upload_to='lesson/%Y/%m/')
    image = CloudinaryField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.subject} - {self.course}'


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.lesson}'

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255)

    def __str__(self):
        return f'{super(Comment, self).__str__()} - {self.content}'


class Like(Interaction):
    class Meta:
        unique_together = ('user', 'lesson')
