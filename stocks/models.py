from django.db import models

class Stock(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class MonthlyData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='monthly_data')
    date = models.DateField()  # Month-end or first day of month representing the month
    dividend = models.FloatField()
    closing_price = models.FloatField()
    dividend_yield = models.FloatField()

    class Meta:
        ordering = ['-date']
        unique_together = ('stock', 'date')

    def __str__(self):
        return f"{self.stock.code} - {self.date}"
