# Generated by Django 5.1.1 on 2024-10-25 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foro', '0009_comentario_no_comentario_si_tema_no_tema_si'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoriausuario',
            old_name='tipo',
            new_name='sede',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]