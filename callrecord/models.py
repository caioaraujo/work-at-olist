from django.db import models
from django.utils import timezone


class CallRecord(models.Model):

    TYPE_CHOICES = [('START', 'Start'),
                    ('END', 'End')]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    call_id = models.PositiveIntegerField()
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)
    price = models.DecimalField(max_digits=13, decimal_places=2, null=True)

    class Meta:
        db_table = 'call_record'
        ordering = ['-id']
