from django.db import models


class TelephoneBill(models.Model):

    id = models.AutoField(primary_key=True)
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)
    call_start_date = models.DateField()
    call_start_time = models.TimeField()
    call_duration = models.CharField(max_length=20)
    call_price = models.DecimalField(max_digits=13, decimal_places=2)

    class Meta:
        db_table = 'telephone_bill'
        ordering = ['-year', '-month']
