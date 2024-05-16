# Generated by Django 5.0.1 on 2024-02-07 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0008_product_seller_colour'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commission_email', models.EmailField(max_length=255)),
                ('seller_name', models.CharField(max_length=255)),
                ('commission_plan', models.CharField(choices=[('zero', 'Zero Commission'), ('subscription', 'Subscription'), ('standard', 'Standard')], max_length=20)),
                ('product_category', models.CharField(blank=True, choices=[('TS', 'Clothes'), ('AC', 'Accessories'), ('BK', 'Books'), ('PT', 'Painting')], max_length=50, null=True)),
                ('product_commission_percent', models.CharField(blank=True, max_length=50, null=True)),
                ('commission_type', models.CharField(blank=True, choices=[('annually', 'Annually'), ('monthly', 'Monthly')], max_length=20, null=True)),
                ('product_commission_rupees', models.CharField(blank=True, max_length=50, null=True)),
                ('commission_approved', models.BooleanField(default=False)),
                ('commission_reject', models.BooleanField(default=False)),
            ],
        ),
    ]