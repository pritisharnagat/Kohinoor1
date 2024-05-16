# Generated by Django 5.0.1 on 2024-04-10 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0014_faqs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateField()),
                ('event_name', models.CharField(blank=True, max_length=200, null=True)),
                ('event_discount', models.FloatField(default=0.0)),
            ],
        ),
    ]
