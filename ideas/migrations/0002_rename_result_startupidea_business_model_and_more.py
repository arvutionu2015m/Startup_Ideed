# Generated by Django 4.2.20 on 2025-04-17 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='startupidea',
            old_name='result',
            new_name='business_model',
        ),
        migrations.AddField(
            model_name='startupidea',
            name='target_audience',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='startupidea',
            name='value_proposition',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='startupidea',
            name='public_id',
            field=models.UUIDField(blank=True, null=True, unique=True),
        ),
    ]
