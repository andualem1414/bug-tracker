# Generated by Django 4.2.2 on 2023-07-05 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_alter_ticket_priority_alter_ticket_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('High', 'High'), ('Low', 'Low'), ('None', 'None'), ('Medium', 'Medium')], max_length=40),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.CharField(choices=[('Feature request', 'Feature Request'), ('Other Comments', 'Other Comments'), ('Bugs/Errors', 'Bugs/Errors'), ('Traning/documents request', 'Traning/documents Request')], max_length=40),
        ),
    ]
