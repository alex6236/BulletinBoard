# Generated by Django 4.2.5 on 2023-09-11 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_board', '0004_alter_ad_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='category_ad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_board.category', verbose_name='Категория'),
        ),
    ]