# Generated by Django 5.1.6 on 2025-03-10 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mskr', '0005_rename_create_meep_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meep',
            old_name='created_at',
            new_name='created',
        ),
    ]
