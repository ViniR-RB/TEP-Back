from decimal import Decimal

from django.core.validators import RegexValidator
from django.db import models

from user.models import CustomUser


# Create your models here.
class Stock(models.Model):
    code_validator = RegexValidator(
        regex=r'^[A-Z]{4}\d$',
        message='O Código deve ter pelo menos 4 letras um e um número'
    )
    cnpj_validator = RegexValidator(
        regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
        message='O CNPJ deve estar no formato XX.XXX.XXX/YYYY-ZZ.'
    )
    code = models.CharField(
        max_length=5,
        unique=True,
        validators=[code_validator]
    )
    name_enterprise = models.CharField(max_length=35)
    cnpj = models.CharField(max_length=18,
                            unique=True,
                            validators=[cnpj_validator])
    created_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.code


class Transaction(models.Model):
    OPERATION_CHOICES = [
        ('C', 'Compra'),
        ('V', 'Venda'),
    ]
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    investor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    brokerage = models.FloatField()
    price_unit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    operation = models.CharField(
        max_length=1, choices=OPERATION_CHOICES, default='C')
    tax_b3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)


    def calculate_price_total(self):
        return self.price_unit * self.quantity

    def tax_totals(self):
        return Decimal(self.brokerage) + Decimal(self.tax_b3)


    def calculate_total_value(self):
        purchase_price = Decimal(self.calculate_price_total())
        tax_totals = self.tax_totals()

        if self.operation == 'C':
           
            return purchase_price + tax_totals
        elif self.operation == 'V':
            
            return purchase_price - tax_totals
    def calculate_price_medium(self):
        return self.calculate_total_value() / self.quantity


    def save(self, *args, **kwargs):
        self.price_total = self.calculate_price_total()
        self.total_value = self.calculate_total_value()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction: {self.date} - {self.stock} - {self.quantity} shares - Brokerage: {self.brokerage} - B3 {self.tax_b3}"
