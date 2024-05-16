# Generated by Django 5.0.1 on 2024-03-18 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0016_orderplaced_razorpay_order_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_src', models.ImageField(blank=True, default='', null=True, upload_to='customize')),
                ('tshirt_size', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('jsonfiles', models.FileField(blank=True, default=None, null=True, upload_to='json_files')),
                ('t_shirt_color', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('tshirt_owndesign_s', models.ImageField(blank=True, default='', null=True, upload_to='customize')),
            ],
        ),
    ]
