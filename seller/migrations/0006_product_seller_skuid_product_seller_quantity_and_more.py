# Generated by Django 5.0.1 on 2024-02-02 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0005_product_seller_actual_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_seller',
            name='SKUId',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='product_seller',
            name='quantity',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product_seller',
            name='size',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
