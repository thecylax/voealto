# Generated by Django 5.1.6 on 2025-02-14 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_rename_client_budget_client_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='budget',
            old_name='client_id',
            new_name='client',
        ),
    ]
