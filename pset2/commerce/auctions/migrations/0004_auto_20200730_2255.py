# Generated by Django 3.0.8 on 2020-07-31 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='image',
            new_name='imgurl',
        ),
    ]