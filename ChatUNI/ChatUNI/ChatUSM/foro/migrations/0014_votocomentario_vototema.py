# Generated by Django 5.1.1 on 2024-10-25 20:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foro', '0013_rename_clase_usuario_categoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='VotoComentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voto', models.BooleanField()),
                ('comentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foro.comentario')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('usuario', 'comentario')},
            },
        ),
        migrations.CreateModel(
            name='VotoTema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voto', models.BooleanField()),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foro.tema')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('usuario', 'tema')},
            },
        ),
    ]
