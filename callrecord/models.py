from django.db import models


class CallRecord(models.Model):

    TYPE_CHOICES = [('START', 'Start'),
                    ('END', 'End')]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField()
    call_id = models.PositiveIntegerField()
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)

    class Meta:
        db_table = 'call_record'
        ordering = ['-id']
