# Generated by Django 4.2.2 on 2023-06-26 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_transaction_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
