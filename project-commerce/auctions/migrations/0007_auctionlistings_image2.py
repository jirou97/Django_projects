# Generated by Django 3.0.1 on 2020-10-17 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201017_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlistings',
            name='image2',
            field=models.FilePathField(default='avatars/avatar.png', verbose_name='image'),
        ),
    ]