# Generated by Django 3.2.9 on 2021-11-10 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20211109_1737'),
    ]

    operations = [
        migrations.CreateModel(
            name='PassportFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tg_id', models.IntegerField()),
                ('path', models.CharField(max_length=255)),
            ],
        ),
    ]
