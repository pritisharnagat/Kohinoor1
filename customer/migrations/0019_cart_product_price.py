# Generated by Django 5.0.1 on 2024-04-04 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0018_orderplaced_image_src_orderplaced_jsonfiles_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='product_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]