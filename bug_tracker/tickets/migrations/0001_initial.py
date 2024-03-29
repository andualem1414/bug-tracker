# Generated by Django 4.2.1 on 2023-06-25 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0006_remove_project_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('new', 'new'), ('open', 'open'), ('inprogress', 'inprogress'), ('resolved', 'resolved'), ('additional information required', 'additional information required')], max_length=40)),
                ('priority', models.CharField(choices=[('Medium', 'Medium'), ('High', 'High'), ('None', 'None'), ('Low', 'Low')], max_length=40)),
                ('type', models.CharField(choices=[('Other Comments', 'Other Comments'), ('Feature request', 'Feature Request'), ('Traning/documents request', 'Traning/documents Request'), ('Bugs/Errors', 'Bugs/Errors')], max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='developer', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('submitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ticket', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.ticket')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
