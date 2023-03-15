from django.test import TestCase

from model_bakery import baker

from api.models.ports import Port

from utils.managers.port_manager import PortManager


class TestPortManager(TestCase):

    def prepare_port_data(self):
        port_codes = ['ABCDE', 'ABCDF', 'ABCDG']
        for code in port_codes:
            baker.make(Port, code=code)

    def prepare_test_dataset(self):
        return [
            {
                'code': 'ABCDE',
                'expected': ['ABCDE']
            },
            {
                'code': 'ABCDEFG',
                'expected': Exception,
                'raise_exception': True
            },
            {
                'code': 'ABCDG',
                'expected': ['ABCDG']
            }
        ]

    def setUp(self):
        self.manager = PortManager()
        self.prepare_port_data()

        self.test_dataset = self.prepare_test_dataset()

    def test_get_port_list_by_code(self):
        for test_data in self.test_dataset:
            if test_data.get('raise_exception', False):
                self.assertRaises(
                    test_data['expected'],
                    self.manager.get_port_list_by_code,
                    test_data['code']
                )
            else:
                self.assertEqual(
                    test_data['expected'],
                    self.manager.get_port_list_by_code(test_data['code'])
                )
