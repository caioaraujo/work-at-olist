from model_mommy import mommy


class Fixtures:

    @staticmethod
    def create_call_record_fixtures():
        mommy.make('callrecord.CallRecord', id=1, type='START',
                   call_id=9, source='1111111111', destination='2222222222',
                   timestamp='2012-01-02 05:11:19')
        mommy.make('callrecord.CallRecord', id=2, type='START',
                   call_id=20, source='2222222222', destination='1111111111')
        mommy.make('callrecord.CallRecord', id=3, type='END',
                   call_id=20, source='2222222222', destination='1111111111')
        mommy.make('callrecord.CallRecord', id=4, type='START',
                   call_id=21, source='4444444444', destination='5555555555',
                   timestamp='2012-01-02 21:57:13')
