# Generated by Django 4.2.2 on 2023-06-13 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_stock_created_at_transaction_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='price_unit',
            field=models.FloatField(null=True),
        ),
    ]
