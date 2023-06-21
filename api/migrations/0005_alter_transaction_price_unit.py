# Generated by Django 4.2.2 on 2023-06-13 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_transaction_price_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='price_unit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
