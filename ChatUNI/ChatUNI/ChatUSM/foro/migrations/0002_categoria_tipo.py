# Generated by Django 5.1.1 on 2024-09-24 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='tipo',
            field=models.CharField(default='', max_length=255),
        ),
    ]
