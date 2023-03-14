from django.db import models


class Region(models.Model):
    slug = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=128)
    parent_slug = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='child_slug', blank=True, null=True
    )

    class Meta:
        db_table = 'regions'
        ordering = ['slug']