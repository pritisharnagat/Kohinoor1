# Generated by Django 5.0.4 on 2024-04-26 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0020_product_seller_discount_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_seller',
            name='bullet_point',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='product_seller',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='product_seller',
            name='special_feature',
            field=models.CharField(blank=True, default='', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='product_seller',
            name='title',
            field=models.CharField(blank=True, max_length=700, null=True),
        ),
    ]