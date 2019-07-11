from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import NotAcceptable, APIException

from telephonebill.services import TelephoneBillService
from .models import CallRecord


class CallRecordService:

    SOURCE = 'Source'
    DESTINATION = 'Destination'
    START = 'START'
    END = 'END'

    def insert_call_start(self, source, destination):
        """
        Save a new call start record

        Args:
            source: source phone number (string)
            destination: destination phone number (string)

        Returns: CallRecord model instance result

        """

        return self._save_call(self.START, source, destination)

    @transaction.atomic
    def insert_call_end(self, source, destination):
        """
        Save a new call end and the telephone bill record

        Args:
            source: source phone number (string)
            destination: destination phone number (string)

        Returns: CallRecord model instance result

        """

        call_record = self._save_call(self.END, source, destination)

        call_id = call_record.call_id
        timestamp_start = (CallRecord.objects
                           .values_list('timestamp', flat=True)
                           .get(call_id=call_id, type=self.START))
        timestamp_end = call_record.timestamp

        telephone_bill_service = TelephoneBillService()
        telephone_bill_service.save_telephone_bill(
            source, destination, timestamp_start, timestamp_end)

        return call_record

    def _save_call(self, call_record_type, source, destination):
        self._validate_phone_number(source, self.SOURCE)
        self._validate_phone_number(destination, self.DESTINATION)

        if source == destination:
            raise NotAcceptable(
                detail='Source and destination must be different')

        call_id = self._get_call_id(call_record_type, source, destination)
        timestamp = timezone.now()

        call_record = CallRecord(
            call_id=call_id, type=call_record_type,
            source=source, destination=destination,
            timestamp=timestamp)

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
