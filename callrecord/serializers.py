from rest_framework import serializers

from .models import CallRecord


class CallStartRecordSerializer(serializers.ModelSerializer):

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

    class Meta:
        model = CallRecord
        fields = ('id', 'type', 'timestamp', 'call_id', 'source',
                  'destination')
        read_only_fields = ('id', 'type', 'timestamp', 'call_id')
