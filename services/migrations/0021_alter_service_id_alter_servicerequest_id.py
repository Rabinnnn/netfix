# Generated by Django 4.2.7 on 2025-02-19 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0020_auto_20250219_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
