# Generated by Django 5.0.1 on 2024-01-19 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0004_product_seller_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_seller',
            name='actual_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='product_seller',
            name='discount_type',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]