from django.db import models


class CallRecord(models.Model):

    TYPE_CHOICES = [('START', 'Start'),
                    ('STOP', 'Stop')]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    call_id = models.PositiveIntegerField()
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)

    class Meta:
        db_table = 'call_record'
        ordering = ['-id']
