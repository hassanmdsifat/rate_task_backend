from django.db import models

from api.models.ports import Port


class Price(models.Model):
    orig_code = models.ForeignKey(
        Port, on_delete=models.CASCADE,
        related_name='origin_prices', db_column='orig_code'
    )
    dest_code = models.ForeignKey(
        Port, on_delete=models.CASCADE,
        related_name='dest_prices', db_column='dest_code'
    )
    day = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'prices'
        ordering = ['-day']