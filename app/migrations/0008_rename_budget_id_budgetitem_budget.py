# Generated by Django 5.1.6 on 2025-02-14 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_budget_budget_items'),
    ]

    operations = [
        migrations.RenameField(
            model_name='budgetitem',
            old_name='budget_id',
            new_name='budget',
        ),
    ]
