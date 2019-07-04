from model_mommy import mommy


class Fixtures:

    @staticmethod
    def create_call_record_fixtures():
        mommy.make('callrecord.CallRecord', id=1, type='START',
                   call_id=9, source='11111', destination='22222')
        mommy.make('callrecord.CallRecord', id=2, type='START',
                   call_id=20, source='22222', destination='11111')
        mommy.make('callrecord.CallRecord', id=3, type='STOP',
                   call_id=20, source='22222', destination='11111')
