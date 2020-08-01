# Generated by Django 3.0.8 on 2020-08-01 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20200801_0103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listing',
        ),
        migrations.AlterField(
            model_name='listing',
            name='bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listbiddings', to='auctions.Bid'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='itemsincategory', to='auctions.Category'),
        ),
        migrations.CreateModel(
            name='BidListings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidlistings', to='auctions.Bid')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listingbids', to='auctions.Listing')),
            ],
        ),
    ]