# Generated by Django 3.1.14 on 2025-02-11 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_alter_service_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
