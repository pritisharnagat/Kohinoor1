# Generated by Django 5.0.4 on 2024-04-25 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0015_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collections_Thought',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('heading', models.CharField(blank=True, max_length=100, null=True)),
                ('heading1', models.CharField(blank=True, max_length=100, null=True)),
                ('heading2', models.CharField(blank=True, max_length=100, null=True)),
                ('heading3', models.CharField(blank=True, max_length=100, null=True)),
                ('heading4', models.CharField(blank=True, max_length=100, null=True)),
                ('heading5', models.CharField(blank=True, max_length=100, null=True)),
                ('heading6', models.CharField(blank=True, max_length=100, null=True)),
                ('paragraph1', models.CharField(blank=True, max_length=500, null=True)),
                ('paragraph2', models.CharField(blank=True, max_length=500, null=True)),
                ('paragraph3', models.CharField(blank=True, max_length=500, null=True)),
                ('paragraph4', models.CharField(blank=True, max_length=500, null=True)),
                ('paragraph5', models.CharField(blank=True, max_length=500, null=True)),
                ('paragraph6', models.CharField(blank=True, max_length=500, null=True)),
                ('paragraph7', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RazorpaySettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_key_id', models.CharField(blank=True, max_length=100, null=True)),
                ('rezorpay_key_secret', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
