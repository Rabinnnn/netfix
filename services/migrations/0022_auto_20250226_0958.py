# Generated by Django 3.1.14 on 2025-02-26 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0021_alter_service_id_alter_servicerequest_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
