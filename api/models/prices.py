from django.db import models

from api.models.ports import Port


class Price(models.Model):
    orig_code = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='origin_prices')
    dest_code = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='dest_prices')
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'prices'
        ordering = ['-date']