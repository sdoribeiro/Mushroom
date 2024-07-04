from django.db import models

# Create your models here.

class Asset(models.Model):
    ticker = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"f{self.id}: ticker {self.ticker} price {self.price}"


class Portifolio (models.Model):
    name = models.CharField(max_length=50)
    ticker = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="asset")
    classification = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.name} ticker {self.ticker} Classification {self.classification}"