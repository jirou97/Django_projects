# Generated by Django 3.0.1 on 2020-10-17 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20201017_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image2',
            field=models.FilePathField(default='/images/avatar.png', verbose_name='image'),
        ),
    ]
