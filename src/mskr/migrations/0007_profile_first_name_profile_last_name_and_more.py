# Generated by Django 5.1.6 on 2025-03-14 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mskr', '0006_rename_created_at_meep_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default='msk_user', max_length=30),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(default='msk_user', max_length=30),
        ),
        migrations.AlterField(
            model_name='meep',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
