# Generated by Django 5.1.6 on 2025-02-15 12:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_rename_budget_id_budgetitem_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ContextItem',
        ),
    ]
