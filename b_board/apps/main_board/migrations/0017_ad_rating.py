# Generated by Django 4.2.5 on 2023-09-29 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_board', '0016_alter_dislike_options_alter_like_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='rating',
            field=models.SmallIntegerField(default=0, verbose_name='Рейтинг'),
        ),
    ]
