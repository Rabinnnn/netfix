# Generated by Django 3.2.20 on 2025-02-03 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_company_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='field',
            new_name='field_of_work',
        ),
        migrations.AddField(
            model_name='company',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
        migrations.AddField(
            model_name='company',
            name='location',
            field=models.CharField(default='', max_length=255),
        ),
    ]
