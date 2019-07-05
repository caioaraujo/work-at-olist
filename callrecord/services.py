from rest_framework.exceptions import NotAcceptable, APIException

from .models import CallRecord


class CallRecordService:

    SOURCE = 'Source'
    DESTINATION = 'Destination'

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

        if 'START' == call_record_type:
            # Find the last call id from a call start record
            last_call_id = (CallRecord.objects
                            .values_list('call_id', flat=True)
                            .order_by('id').last())
            if not last_call_id:
                # It is the first call record in the database
                return 1
            return last_call_id+1

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
