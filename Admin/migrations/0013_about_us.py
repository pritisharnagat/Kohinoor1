# Generated by Django 5.0.1 on 2024-04-09 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0012_emailsetting'),
    ]

    operations = [
        migrations.CreateModel(
            name='about_us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.TextField(blank=True, default='', null=True)),
                ('vision', models.TextField(blank=True, default='', null=True)),
                ('mission', models.TextField(blank=True, default='', null=True)),
            ],
        ),
    ]