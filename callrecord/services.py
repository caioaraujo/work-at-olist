from datetime import timedelta

from rest_framework.exceptions import NotAcceptable, APIException

from .models import CallRecord


class CallRecordService:

    SOURCE = 'Source'
    DESTINATION = 'Destination'
    START = 'START'
    END = 'END'
    STANDING_CHARGE = 0.36
    CHARGE_MINUTE = 0.09

    def insert(self, call_record_type, source, destination):
        """
        Save a new call record

        Args:
            call_record_type: string 'START' or 'END'
            source: source phone number (string)
            destination: destination phone number (string)

        Returns: CallRecord model instance result

        """

        self._validate_phone_number(source, self.SOURCE)
        self._validate_phone_number(destination, self.DESTINATION)

        if source == destination:
            raise NotAcceptable(
                detail='Source and destination must be different')

        call_id = self._get_call_id(call_record_type, source, destination)

        call_record = CallRecord(
            call_id=call_id, type=call_record_type,
            source=source, destination=destination)

        call_record.save()

        return call_record

    def _get_call_id(self, call_record_type, source, destination):
        """ Returns a new call id when call_record_type is 'START'. Otherwise,
            find the call id from the last call record start between the source
            and destination.
         """

        if self.START == call_record_type:
            return self._get_call_id_start()

        return self._get_call_id_end(source, destination)

    def _get_call_id_start(self):
        # Find the last call id from a call start record
        last_call_id = (CallRecord.objects
                        .values_list('call_id', flat=True)
                        .order_by('id').last())
        if not last_call_id:
            # It is the first call record in the database
            return 1
        return last_call_id + 1

    def _get_call_id_end(self, source, destination):
        # Find the call id from the last call start between source
        # and destination
        last_call_id = (CallRecord.objects
                        .values_list('call_id', flat=True)
                        .filter(source=source, destination=destination)
                        .order_by('id').last())

        if not last_call_id:
            raise APIException(
                detail=f'Start record not found for source {source} '
                f'and destination {destination}')

        return last_call_id

    def _validate_phone_number(self, phone_number, origin):
        """
        Validate phone number data from source and destination (origin)
        """
        if not phone_number:
            raise NotAcceptable(detail=f'{origin} is required')
        if not phone_number.isdigit():
            raise NotAcceptable(detail=f'{origin} must be numeric')
        if len(phone_number) < 10:
            raise NotAcceptable(
                detail=f'{origin} must have at least 10 numbers')
        if len(phone_number) > 11:
            raise NotAcceptable(
                detail=f'{origin} must have a maximum of 11 numbers')

    def calculate_call_price(self, call_id):
        """
        Calculate the call price

        Args:
            call_id: id which represents both start and end call

        Returns: The price in float

        """

        # Find the timestamp of the call start record
        timestamp_start = self._get_call_timestamp(call_id, self.START)

        # Find the timestamp of the call end record
        timestamp_end = self._get_call_timestamp(call_id, self.END)

        # Find the total of minutes between these dates
        diff_time = timestamp_end - timestamp_start
        charged_minutes = diff_time.seconds//60

        # Set zero to seconds from both dates
        timestamp_start = timestamp_start.replace(second=0, microsecond=0)
        timestamp_end = timestamp_end.replace(second=0, microsecond=0)

        while timestamp_start != timestamp_end:

            if timestamp_start.hour > 21 or timestamp_start.hour < 6:
                # Unconsider the current minute if it is in the
                # reduced tariff time call (22pm to 5:59am)
                charged_minutes -= 1
            # Increment one minute do timestamp_start
            timestamp_start = timestamp_start + timedelta(minutes=1)

        # Return the final price
        return charged_minutes * self.CHARGE_MINUTE + self.STANDING_CHARGE

    def _get_call_timestamp(self, call_id, call_type):
        return (CallRecord.objects.values_list('timestamp', flat=True)
                .get(call_id=call_id, type=call_type))
