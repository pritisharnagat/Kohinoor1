# Generated by Django 5.0.1 on 2024-04-09 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0013_about_us'),
    ]

    operations = [
        migrations.CreateModel(
            name='faqs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('answers', models.TextField(blank=True, default='', null=True)),
            ],
        ),
    ]
