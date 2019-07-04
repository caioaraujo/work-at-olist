from .models import CallRecord


class CallRecordService:

    def insert(self, call_record_type, source, destination):

        call_id = self._get_call_id(call_record_type, source, destination)

        call_record = CallRecord(call_id=call_id, type=call_record_type,
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
        return last_call_id
