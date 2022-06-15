# Generated by Django 3.2.5 on 2022-06-12 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_userprofile_langs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='about',
            field=models.TextField(blank=True, verbose_name='О себе'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'М'), ('f', 'Ж')], max_length=2, verbose_name='Пол'),
        ),
    ]
