# Generated by Django 5.0.1 on 2024-03-09 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_vruser_company_address_vruser_company_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscribedEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
