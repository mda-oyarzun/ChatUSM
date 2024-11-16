# Generated by Django 5.1.1 on 2024-09-25 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foro', '0004_solicitudeliminaciontema'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField()),
                ('tipo', models.CharField(default='', max_length=255)),
            ],
        ),
    ]