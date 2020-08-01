# Generated by Django 3.0.8 on 2020-08-01 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20200731_2319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='price',
            new_name='startingprice',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='highestbidder',
        ),
        migrations.AddField(
            model_name='listing',
            name='bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidlistings', to='auctions.Bid'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listingbids', to='auctions.Listing'),
        ),
    ]
