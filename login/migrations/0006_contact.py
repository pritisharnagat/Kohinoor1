# Generated by Django 5.0.1 on 2024-01-23 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_seller_user_commision_seller_user_seller_approved_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('comment', models.TextField(max_length=200)),
            ],
        ),
    ]