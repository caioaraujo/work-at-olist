from model_mommy import mommy


class Fixtures:

    @staticmethod
    def create_call_record_fixtures():
        mommy.make('callrecord.CallRecord', id=1, type='START',
                   call_id=9, source='1111111111', destination='2222222222')
        mommy.make('callrecord.CallRecord', id=2, type='START',
                   call_id=20, source='2222222222', destination='1111111111')
        mommy.make('callrecord.CallRecord', id=3, type='END',
                   call_id=20, source='2222222222', destination='1111111111')
