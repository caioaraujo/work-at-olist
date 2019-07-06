from datetime import datetime

from django.test import TestCase, SimpleTestCase
from rest_framework.exceptions import NotAcceptable, APIException

from ..services import CallRecordService
from .fixtures import Fixtures


class TestCallRecordService(TestCase):
    """
    Service class unit tests which opens database connection
    """

    def setUp(self):
        self.service = CallRecordService()

    def test_get_call_id__first_database_record(self):
        call_record_type = 'START'
        source = '2222222'
        destination = '111111'

        call_id = self.service._get_call_id(
            call_record_type, source, destination)
        self.assertEqual(1, call_id)

    def test_get_call_id__call_type_start(self):
        # Install fixtures
        Fixtures.create_call_record_fixtures()

        call_record_type = 'START'
        source = '2222222222'
        destination = '1111111111'

        call_id = self.service._get_call_id(
            call_record_type, source, destination)
        self.assertEqual(25, call_id)

    def test_get_call_id__call_type_end(self):
        # Install fixtures
        Fixtures.create_call_record_fixtures()

        call_record_type = 'END'
        source = '1111111111'
        destination = '2222222222'

        call_id = self.service._get_call_id(
            call_record_type, source, destination)
        self.assertEqual(9, call_id)

    def test_get_call_id__start_call_not_found(self):
        call_record_type = 'END'
        source = '1111111111'
        destination = '2222222222'

        with self.assertRaisesMessage(
                APIException,
                'Start record not found for source 1111111111 '
                'and destination 2222222222'):
            self.service._get_call_id(
                call_record_type, source, destination)

    def test_calculate_call_price__between_tariff_periods(self):
        # Install fixtures
        Fixtures.create_call_record_fixtures()

        timestamp_end = datetime(2012, 1, 2, 22, 17, 53)
        price = self.service._calculate_call_price(
            call_id=21, timestamp_end=timestamp_end)
        self.assertEqual(price, 0.54)

    def test_calculate_call_price__less_than_one_minute(self):
        # Install fixtures
        Fixtures.create_call_record_fixtures()

        timestamp_end = datetime(2012, 1, 2, 7, 10, 59)
        price = self.service._calculate_call_price(
            call_id=22, timestamp_end=timestamp_end)
        self.assertEqual(price, 0.36)

    def test_calculate_call_price__exactly_one_minute(self):
        # Install fixtures
        Fixtures.create_call_record_fixtures()

        timestamp_end = datetime(2012, 1, 2, 7, 11, 2)
        price = self.service._calculate_call_price(
            call_id=23, timestamp_end=timestamp_end)
        self.assertEqual(price, 0.45)

    def test_calculate_call_price__over_one_minute(self):
        # Install fixtures
        Fixtures.create_call_record_fixtures()

        timestamp_end = datetime(2012, 1, 2, 7, 12, 1)
        price = self.service._calculate_call_price(
            call_id=24, timestamp_end=timestamp_end)
        self.assertEqual(price, 0.45)


class TestCallRecordServiceWithoutDBConnection(SimpleTestCase):
    """
    Service class unit tests which doesn't open database connection
    """

    def setUp(self):
        self.service = CallRecordService()

    def test_validate_phone_number__source_required(self):

        with self.assertRaisesMessage(NotAcceptable, 'Source is required'):
            self.service._validate_phone_number(None, self.service.SOURCE)

    def test_validate_phone_number__source_is_non_numeric(self):

        with self.assertRaisesMessage(NotAcceptable, 'Source must be numeric'):
            self.service._validate_phone_number(
                '48-11111', self.service.SOURCE)

    def test_validate_phone_number__source_is_too_small(self):

        with self.assertRaisesMessage(
                NotAcceptable, 'Source must have at least 10 numbers'):
            self.service._validate_phone_number(
                '4811111', self.service.SOURCE)

    def test_validate_phone_number__source_is_too_large(self):

        with self.assertRaisesMessage(
                NotAcceptable, 'Source must have a maximum of 11 numbers'):
            self.service._validate_phone_number(
                '481111111111111111111', self.service.SOURCE)

    def test_validate_phone_number__destination_required(self):

        with self.assertRaisesMessage(
                NotAcceptable, 'Destination is required'):
            self.service._validate_phone_number(None, self.service.DESTINATION)

    def test_validate_phone_number__destination_is_non_numeric(self):

        with self.assertRaisesMessage(
                NotAcceptable, 'Destination must be numeric'):
            self.service._validate_phone_number(
                '48-11111', self.service.DESTINATION)

    def test_validate_phone_number__destination_is_too_small(self):

        with self.assertRaisesMessage(
                NotAcceptable, 'Destination must have at least 10 numbers'):
            self.service._validate_phone_number(
                '4811111', self.service.DESTINATION)

    def test_validate_phone_number__destination_is_too_large(self):

        with self.assertRaisesMessage(
                NotAcceptable,
                'Destination must have a maximum of 11 numbers'):
            self.service._validate_phone_number(
                '481111111111111111111', self.service.DESTINATION)

    def test_validate_phone_number__same_number(self):
        source = '1111111111'
        destination = '1111111111'

        with self.assertRaisesMessage(
                NotAcceptable,
                'Source and destination must be different'):
            self.service.insert('START', source, destination)
