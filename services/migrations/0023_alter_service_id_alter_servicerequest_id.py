# Generated by Django 5.1.6 on 2025-02-27 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0022_auto_20250226_0958'),
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
