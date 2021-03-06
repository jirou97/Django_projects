# Generated by Django 3.1.7 on 2021-09-05 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20210905_1812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='post',
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='network.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
