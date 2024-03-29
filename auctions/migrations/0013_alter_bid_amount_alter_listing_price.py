# Generated by Django 4.1.6 on 2023-03-27 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_listing_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
