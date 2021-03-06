# Generated by Django 3.0.8 on 2020-07-31 23:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200731_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='highestbidder',
            field=models.CharField(default=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL), max_length=80),
        ),
        migrations.AddField(
            model_name='listing',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]
