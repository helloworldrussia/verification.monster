# Generated by Django 3.2.9 on 2021-11-04 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default="None", max_length=50, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default="None", max_length=50, verbose_name='Фамилия'),
        ),
    ]
