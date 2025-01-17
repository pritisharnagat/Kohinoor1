# Generated by Django 5.0.1 on 2024-03-13 06:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0012_orderplaced_cod_amount'),
        ('login', '0009_subscribedemail'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customize_product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_src', models.ImageField(blank=True, default='', null=True, upload_to='customize')),
                ('tshirt_size', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('jsonfiles', models.FileField(blank=True, default=None, null=True, upload_to='json_files')),
                ('t_shirt_color', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('tshirt_owndesign_s', models.ImageField(blank=True, default='', null=True, upload_to='customize')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.customer_user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
