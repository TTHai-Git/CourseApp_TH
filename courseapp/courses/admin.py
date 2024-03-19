import cloudinary
from django.contrib import admin
from django import forms
from courses.models import *
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Register your models here.

class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'


class MyCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'created_date', 'updated_date', 'active']
    search_fields = ['subject', 'description']
    list_filter = ['id', 'created_date', 'subject']
    readonly_fields = ['my_image']
    form = CourseForm

    def my_image(self, instance):
        if instance:
            if instance.image is cloudinary.CloudinaryResource:
                return mark_safe(f"<img width='120' src='{instance.image.url}' />")

            return mark_safe(f"<img width='120' src='/static/{instance.image.name}' />")


admin.site.register(Category)
admin.site.register(Course, MyCourseAdmin)
admin.site.register(Lesson)
admin.site.register(User)
admin.site.register(Tag)
