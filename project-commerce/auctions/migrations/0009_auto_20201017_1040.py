# Generated by Django 3.0.1 on 2020-10-17 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20201017_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='image',
        ),
        migrations.AlterField(
            model_name='user',
            name='image2',
            field=models.FilePathField(default='auctions/avatars/avatar.png', verbose_name='image'),
        ),
    ]
