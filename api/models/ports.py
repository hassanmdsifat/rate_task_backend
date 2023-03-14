from django.db import models

from api.models.regions import Region


class Port(models.Model):
    parent_slug = models.ForeignKey(
        Region, on_delete=models.CASCADE,
        related_name='ports', db_column='parent_slug'
    )

    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=128)

    class Meta:
        db_table='ports'
        ordering = ['name']