from datetime import datetime

from django.test import SimpleTestCase

from ..services import TelephoneBillService


class TestTelephoneBillServiceWithoutDBConnection(SimpleTestCase):
    """
    Service class unit tests which doesn't open database connection
    """

    def setUp(self):
        self.service = TelephoneBillService()

    def test_calculate_call_price__between_tariff_periods(self):
        timestamp_start = datetime(2012, 1, 2, 21, 57, 13)
        timestamp_end = datetime(2012, 1, 2, 22, 17, 53)
        price = self.service._calculate_call_price(
            timestamp_start=timestamp_start,
            timestamp_end=timestamp_end)
        self.assertEqual(price, 0.54)

    def test_calculate_call_price__less_than_one_minute(self):
        timestamp_start = datetime(2012, 1, 2, 7, 10, 1)
        timestamp_end = datetime(2012, 1, 2, 7, 10, 59)
        price = self.service._calculate_call_price(
            timestamp_start=timestamp_start,
            timestamp_end=timestamp_end)
        self.assertEqual(price, 0.36)

    def test_calculate_call_price__exactly_one_minute(self):
        timestamp_start = datetime(2012, 1, 2, 7, 10, 2)
        timestamp_end = datetime(2012, 1, 2, 7, 11, 2)
        price = self.service._calculate_call_price(
            timestamp_start=timestamp_start,
            timestamp_end=timestamp_end)
        self.assertEqual(price, 0.45)

    def test_calculate_call_price__over_one_minute(self):
        timestamp_start = datetime(2012, 1, 2, 7, 10, 2)
        timestamp_end = datetime(2012, 1, 2, 7, 12, 1)
        price = self.service._calculate_call_price(
            timestamp_start=timestamp_start,
            timestamp_end=timestamp_end)
        self.assertEqual(price, 0.45)

    def test_set_zero_to_seconds(self):
        timestamp = datetime(2019, 1, 1, 13, 48, 34)
        expected_timestamp = datetime(2019, 1, 1, 13, 48, 0)
        obtained_timestamp = self.service._set_zero_to_seconds(timestamp)

        self.assertEqual(expected_timestamp, obtained_timestamp)

    def test_calculate_call_duration(self):
        timestamp_start = datetime(2019, 1, 1, 13, 48, 34)
        timestamp_end = datetime(2019, 1, 2, 14, 49, 36)

        obtained_duration = self.service._calculate_call_duration(
            timestamp_start, timestamp_end)
        expected_duration = '25:01:02'

        self.assertEqual(expected_duration, obtained_duration)
