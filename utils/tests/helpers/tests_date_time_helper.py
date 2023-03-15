from datetime import datetime

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from utils.helpers.date_time_helpers import parse_date_from_string, parse_date_from_datetime


class TestDateTimeHelper(TestCase):

    def setUp(self):
        self.string_dataset = [
            {
                'value': '2018-03-31',
                'expected': datetime(year=2018, month=3, day=31),
            },
            {
                'value': '2018-03-33',
                'expected': ValidationError,
                'raise_exception': True
            },
            {
                'value': '02-03-2019',
                'expected': ValidationError,
                'raise_exception': True
            }
        ]

        self.date_dataset = [
            {
                'value': datetime(year=2018, month=3, day=31),
                'expected': '2018-03-31',
            },
            {
                'value': '2018-03-33',
                'expected': '2018-03-33',
            },
            {
                'value': '02-03-2019',
                'expected': '02-03-2019',
            }
        ]

    def test_parse_date_from_string(self):

        for test_data in self.string_dataset:
            if test_data.get('raise_exception', False):
                self.assertRaises(test_data['expected'], parse_date_from_string, test_data['value'])
            else:
                self.assertEqual(test_data['expected'], parse_date_from_string(test_data['value']))

    def test_parse_date_from_datetime(self):
        for test_data in self.date_dataset:
            self.assertEqual(test_data['expected'], parse_date_from_datetime(test_data['value']))

