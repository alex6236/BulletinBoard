# Generated by Django 4.2.5 on 2023-09-12 00:56

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('main_board', '0005_ad_category_ad'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='ad',
            managers=[
                ('ad_published', django.db.models.manager.Manager()),
            ],
        ),
    ]
