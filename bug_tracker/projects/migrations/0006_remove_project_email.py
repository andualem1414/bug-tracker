# Generated by Django 4.2.1 on 2023-06-17 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_rename_created_project_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='email',
        ),
    ]