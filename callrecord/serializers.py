from rest_framework import serializers

from .models import CallRecord


class CallRecordSerializer(serializers.ModelSerializer):

    source = serializers.CharField(
        help_text='A numeric string representing the source phone number',
        required=True,
        max_length=11)
    destination = serializers.CharField(
        help_text='A numeric string representing the destination phone number',
        required=True,
        max_length=11)
    call_id = serializers.IntegerField(
        help_text='A unique ID that links a start call and an end call '
                  'between a source and a destination',
        read_only=True
    )
    timestamp = serializers.DateTimeField(
        help_text='The timestamp a call was started or ended',
        read_only=True
    )
    price = serializers.DecimalField(
        max_digits=13, decimal_places=2,
        help_text='The call price, calculated in the end record',
        read_only=True
    )

    class Meta:
        model = CallRecord
        fields = ('id', 'type', 'timestamp', 'call_id', 'source',
                  'destination', 'price', )
        read_only_fields = ('id', 'type', 'timestamp', 'call_id', 'price', )
