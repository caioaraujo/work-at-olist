from django.db import transaction
from rest_framework.exceptions import NotAcceptable, APIException

from telephonebill.services import TelephoneBillService
from .models import CallRecord


class CallRecordService:

    SOURCE = 'Source'
    DESTINATION = 'Destination'
    CALL_ID = 'Call id'
    TIMESTAMP = 'Timestamp'
    START = 'START'
    END = 'END'

    def insert_call_start(self, source, destination, call_id, timestamp):
        """
        Save a new call start record

        Args:
            source: source phone number (string)
            destination: destination phone number (string)
            call_id: unique id that identifies start and end call (int)
            timestamp: timestamp of the call record

        Returns: CallRecord model instance result

        """
        self._validate_source_and_destination(source, destination)
        self._validate_call_id(call_id)
        self._validate_required_data(timestamp, self.TIMESTAMP)

        return self._save_call(
            self.START, source, destination, call_id, timestamp)

    @transaction.atomic
    def insert_call_end(self, call_id, timestamp):
        """
        Save a new call end and the telephone bill record

        Args:
            call_id: unique id that identifies start and end call (int)
            timestamp: timestamp of the call record

        Returns: CallRecord model instance result

        """
        self._validate_required_data(call_id, self.CALL_ID)
        self._validate_required_data(timestamp, self.TIMESTAMP)

        start_call = self._get_start_call_by_call_id(call_id)
        source = start_call.source
        destination = start_call.destination

        call_record = self._save_call(
            self.END, source, destination, call_id, timestamp)

        timestamp_start = start_call.timestamp
        timestamp_end = call_record.timestamp

        telephone_bill_service = TelephoneBillService()
        telephone_bill_service.save_telephone_bill(
            source, destination, timestamp_start, timestamp_end)

        return call_record

    def _get_start_call_by_call_id(self, call_id):
        """ Get the CallRecord model instance from the start call """
        start_call = (CallRecord.objects
                      .filter(call_id=call_id, type=self.START))

        if not start_call.exists():
            raise APIException(
                detail=f'Start record not found for call id {call_id}')

        return start_call.first()

    def _save_call(self, call_record_type, source, destination,
                   call_id, timestamp):

        call_record = CallRecord(
            call_id=call_id, type=call_record_type,
            source=source, destination=destination,
            timestamp=timestamp)

        call_record.save()

        return CallRecord.objects.get(id=call_record.id)

    def _validate_source_and_destination(self, source, destination):
        self._validate_phone_number(source, self.SOURCE)
        self._validate_phone_number(destination, self.DESTINATION)

        if source == destination:
            raise NotAcceptable(
                detail='Source and destination must be different')

    def _validate_phone_number(self, phone_number, origin):
        """
        Validate source and destination phone numbers
        """
        self._validate_required_data(phone_number, origin)
        if not phone_number.isdigit():
            raise NotAcceptable(detail=f'{origin} must be numeric')
        if len(phone_number) < 10:
            raise NotAcceptable(
                detail=f'{origin} must have at least 10 numbers')
        if len(phone_number) > 11:
            raise NotAcceptable(
                detail=f'{origin} must have a maximum of 11 numbers')

    def _validate_required_data(self, value, field):

        if not value:
            raise NotAcceptable(detail=f'{field} is required')

    def _validate_call_id(self, call_id):
        """ Validate call id data """

        self._validate_required_data(call_id, self.CALL_ID)

        query = CallRecord.objects.filter(call_id=call_id)

        if query.exists():
            raise NotAcceptable(
                detail='Call id is already in use. Please, choose another')
