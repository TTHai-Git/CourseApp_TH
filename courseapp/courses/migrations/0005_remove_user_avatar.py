# Generated by Django 5.0.3 on 2024-03-20 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_course_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
    ]