# Generated by Django 5.0.1 on 2024-04-06 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0017_product_seller_image_src_product_seller_jsonfiles_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_seller',
            name='product_story',
            field=models.TextField(blank=True, default='', max_length=500, null=True),
        ),
    ]