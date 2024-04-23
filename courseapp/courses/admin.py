import cloudinary
from django.contrib import admin
from django import forms
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path

from courses.models import *
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Register your models here.

class MyAdminSite(admin.AdminSite):
    site_header = 'iCourse'

    def get_urls(self):
        return [path('cate-stats/', self.stats)] + super().get_urls()

    def stats(self, request):
        stats = Category.objects.annotate(counter=Count('course__id')).values('id', 'name', 'counter')
        return TemplateResponse(request, 'admin/stats.html', {
            'stats': stats
        })


admin_site = MyAdminSite(name='iCourse')


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


admin_site.register(Category)
admin_site.register(Course, MyCourseAdmin)
admin_site.register(Lesson)
admin_site.register(User)
admin_site.register(Tag)
admin_site.register(Comment)