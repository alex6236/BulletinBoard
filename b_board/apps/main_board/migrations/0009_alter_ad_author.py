# Generated by Django 4.2.5 on 2023-09-20 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_board', '0008_reply_is_published_alter_reply_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='author_ad', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
