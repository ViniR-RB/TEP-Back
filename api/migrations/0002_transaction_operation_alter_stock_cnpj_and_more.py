# Generated by Django 4.2.2 on 2023-06-06 20:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='operation',
            field=models.CharField(choices=[('C', 'Compra'), ('V', 'Venda')], default='C', max_length=1),
        ),
        migrations.AlterField(
            model_name='stock',
            name='cnpj',
            field=models.CharField(max_length=18, unique=True, validators=[django.core.validators.RegexValidator(message='O CNPJ deve estar no formato XX.XXX.XXX/YYYY-ZZ.', regex='^\\d{2}\\.\\d{3}\\.\\d{3}/\\d{4}-\\d{2}$')]),
        ),
        migrations.AlterField(
            model_name='stock',
            name='code',
            field=models.CharField(max_length=5, unique=True, validators=[django.core.validators.RegexValidator(message='O Código deve ter pelo menos 4 letras um e um número', regex='^[A-Z]{4}\\d$')]),
        ),
    ]
