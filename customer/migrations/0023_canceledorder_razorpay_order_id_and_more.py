# Generated by Django 5.0.4 on 2024-04-25 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0022_canceledorder_invoice_no_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='canceledorder',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='canceledorder',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
