# Generated by Django 3.2.9 on 2021-11-05 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tg_id', models.IntegerField()),
                ('tg_username', models.IntegerField()),
                ('tg_chat_id', models.IntegerField()),
            ],
        ),
    ]
