# Generated by Django 3.2.20 on 2025-02-10 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_auto_20250210_1923'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='price_hour',
            new_name='price_per_hour',
        ),
        migrations.RemoveField(
            model_name='service',
            name='rating',
        ),
    ]
