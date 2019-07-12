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

    def test_start_call_by_call_id__not_found(self):
        call_id = 99

        with self.assertRaisesMessage(
                APIException,
                'Start record not found for call id 99'):
            self.service._get_start_call_by_call_id(call_id)

    def test_start_call_by_call_id__success(self):
        # Install fixtures
        Fixtures.create_call_record_fixtures()

        call_id = 9

        start_call = self.service._get_start_call_by_call_id(call_id)
        self.assertEqual(start_call.id, 1)

    def test_insert_call_end__call_id_required(self):
        with self.assertRaisesMessage(
                NotAcceptable, 'Call id is required'):
            self.service.insert_call_end(None, 'aaa')

    def test_insert_call_end__timestamp_required(self):
        with self.assertRaisesMessage(
                NotAcceptable, 'Timestamp is required'):
            self.service.insert_call_end(22, None)

    def test_validate_call_id__already_in_use(self):
        # Install fixtures
        Fixtures.create_call_record_fixtures()

        with self.assertRaisesMessage(
                NotAcceptable,
                'Call id is already in use. Please, choose another'):
            self.service._validate_call_id(9)

    def test_insert_call_start__timestamp_required(self):
        with self.assertRaisesMessage(
                NotAcceptable, 'Timestamp is required'):
            self.service.insert_call_start(
                '1111111111', '22222222222', 22, None)


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

    def test_insert_call_start__same_number(self):
        source = '1111111111'
        destination = '1111111111'

        with self.assertRaisesMessage(
                NotAcceptable,
                'Source and destination must be different'):
            self.service.insert_call_start(source, destination, 1, 'aaa')

    def test_validate_call_id__required(self):
        with self.assertRaisesMessage(
                NotAcceptable, 'Call id is required'):
            self.service._validate_call_id(None)
