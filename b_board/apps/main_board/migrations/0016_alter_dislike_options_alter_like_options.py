# Generated by Django 4.2.5 on 2023-09-29 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_board', '0015_ad_video'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dislike',
            options={'verbose_name': 'Дизлайк', 'verbose_name_plural': 'Дизлайки'},
        ),
        migrations.AlterModelOptions(
            name='like',
            options={'verbose_name': 'Лайк', 'verbose_name_plural': 'Лайки'},
        ),
    ]
