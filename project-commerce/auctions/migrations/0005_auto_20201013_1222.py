# Generated by Django 3.0.1 on 2020-10-13 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20201011_1928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlistings',
            name='category',
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default=None, max_length=50)),
                ('auction_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.AuctionListings')),
            ],
        ),
    ]
