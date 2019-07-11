from model_mommy import mommy


class Fixtures:

    @staticmethod
    def create_telephone_bill_fixtures():
        mommy.make('telephonebill.TelephoneBill', id=1,
                   source='11111111111', destination='2222222222',
                   year=2018, month=4, call_start_date='2018-04-02',
                   call_start_time='23:34:33', call_duration="00:32:51",
                   call_price="12.66", )
        mommy.make('telephonebill.TelephoneBill', id=2,
                   source='11111111111', destination='3333333333',
                   year=2018, month=5, call_start_date='2018-05-02',
                   call_start_time='06:21:00', call_duration="02:42:02",
                   call_price="0.36", )
        mommy.make('telephonebill.TelephoneBill', id=3,
                   source='11111111111', destination='1212121212',
                   year=2018, month=5, call_start_date='2018-05-22',
                   call_start_time='06:21:00', call_duration="02:42:02",
                   call_price="0.38", )
        mommy.make('telephonebill.TelephoneBill', id=4,
                   source='11111111111', destination='2121212121',
                   year=2018, month=6, call_start_date='2018-06-02',
                   call_start_time='06:21:00', call_duration="02:42:02",
                   call_price="0.39", )
        mommy.make('telephonebill.TelephoneBill', id=5,
                   source='11111111111', destination='2222222111',
                   year=2019, month=1, call_start_date='2019-01-22',
                   call_start_time='06:57:12', call_duration="00:05:00",
                   call_price="0.36", )
        mommy.make('telephonebill.TelephoneBill', id=6,
                   source='1111111111', destination='3333333333',
                   year=2018, month=5, call_start_date='2018-05-02',
                   call_start_time='06:21:00', call_duration="02:42:02",
                   call_price="0.36", )
