# Generated by Django 4.2.2 on 2023-06-26 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_stock_created_at_alter_stock_name_enterprise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
