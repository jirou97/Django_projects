# Generated by Django 3.0.1 on 2020-10-10 09:36

import auctions.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlistings',
            name='expire_time',
            field=models.DateTimeField(default=auctions.models.five_days_later),
        ),
    ]
