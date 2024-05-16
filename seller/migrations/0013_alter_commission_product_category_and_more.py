# Generated by Django 5.0.1 on 2024-03-22 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0012_alter_commission_product_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='product_category',
            field=models.CharField(blank=True, choices=[('TS', 'Clothes'), ('AC', 'Accessories'), ('BK', 'Books'), ('PT', 'Painting'), ('CS', 'Customize'), ('SMQ', 'Shivaji')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='product_seller',
            name='category',
            field=models.CharField(choices=[('TS', 'Clothes'), ('AC', 'Accessories'), ('BK', 'Books'), ('PT', 'Painting'), ('CS', 'Customize'), ('SMQ', 'Shivaji')], max_length=50),
        ),
    ]
