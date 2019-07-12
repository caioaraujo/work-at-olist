from rest_framework import serializers

from .models import CallRecord


class CustomDateTimeField(serializers.DateTimeField):

    def to_representation(self, value):
        datetimerepr = value.strftime("%Y-%m-%d %H:%M:%S")
        return super(CustomDateTimeField, self).to_representation(datetimerepr)


class CallRecordStartSerializer(serializers.ModelSerializer):

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
        required=True
    )
    timestamp = CustomDateTimeField(
        help_text='The timestamp a call was started (eg 2016-02-29T12:00:00Z)',
        required=True
    )

    class Meta:
        model = CallRecord
        fields = ('id', 'type', 'timestamp', 'call_id', 'source',
                  'destination', )
        read_only_fields = ('id', 'type', )


class CallRecordEndSerializer(serializers.ModelSerializer):

    call_id = serializers.IntegerField(
        help_text='A unique ID that links a start call and an end call '
                  'between a source and a destination',
        required=True
    )
    timestamp = CustomDateTimeField(
        help_text='The timestamp a call was ended (eg 2016-02-29T12:00:00Z)',
        required=True
    )

    class Meta:
        model = CallRecord
        fields = ('id', 'type', 'timestamp', 'call_id', 'source',
                  'destination', )
        read_only_fields = ('id', 'type', 'source', 'destination', )
