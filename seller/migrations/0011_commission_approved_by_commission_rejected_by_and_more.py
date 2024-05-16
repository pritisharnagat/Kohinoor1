# Generated by Django 5.0.1 on 2024-02-16 07:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0010_product_seller_prod_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_commissions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commission',
            name='rejected_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rejected_commissions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commission',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='', max_length=20),
        ),
    ]