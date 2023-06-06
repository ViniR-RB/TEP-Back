from django.core.validators import RegexValidator
from django.db import models
from user.models import CustomUser

# Create your models here.
class Stock(models.Model):
    code_validator = RegexValidator(
        regex=r'^[A-Z]{4}\d$',
        message='O CNPJ deve estar no formato XX.XXX.XXX/YYYY-ZZ.'
    )
    cnpj_validator = RegexValidator(
        regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
        message='CNPJ não é válido'
    )
    code = models.CharField(
        max_length=5,
        unique=True,
        validators=[code_validator]
    )
    name_enterprise = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18,
                            unique=True,
                            validators=[cnpj_validator])

    def __str__(self):
        return self.code


class Transaction(models.Model):
    date = models.DateField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    investor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    brokerage = models.FloatField()

    def __str__(self):
        return f"Transaction: {self.date} - {self.stock} - {self.quantity} shares - Brokerage: {self.brokerage}"
