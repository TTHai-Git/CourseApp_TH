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
    list_filter = ['id', 'subject']
    search_fields = ['id', 'subject']
    readonly_fields = ['avatar']

    def avatar(self, obj):
        if obj:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=obj.image.name)
            )
    # class Media:
    #     css = {
    #         'all':('/static/css/style.css', )
    #     }
    form = CourseForm


admin.site.register(Category)
admin.site.register(Course, MyCourseAdmin)
