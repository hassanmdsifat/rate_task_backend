from datetime import datetime

from django.test import TestCase
from model_bakery import baker

from api.models.regions import Region
from api.models.ports import Port
from api.models.prices import Price

from utils.managers.rate_calculator_manager import RateCalculatorManager


class TestRateCalculatorManager(TestCase):

    def prepare_region_data(self):
        region_dataset = [
            {
                'slug': 'region_a',
                'parent_slug_id': None,
            },
            {
                'slug': 'region_1',
                'parent_slug_id': None,
            },
            {
                'slug': 'region_eu',
                'parent_slug_id': None,
            },
            {
                'slug': 'region_us',
                'parent_slug_id': None,
                'ports': ["USP1", "USP2", "USP3", "USP4"]
            },
            {
                'slug': 'region_b',
                'parent_slug_id': 'region_a',
                'ports': ["PORT1", "PORT2", "PORT3"]
            },
            {
                'slug': 'region_c',
                'parent_slug_id': 'region_a',
                'ports': ["PORT4"]
            },
            {
                'slug': 'region_d',
                'parent_slug_id': 'region_c',
                'ports': ["PORT5", "PORT6"]
            },
            {
                'slug': 'region_2',
                'parent_slug_id': 'region_1',
                'ports': ["PORT7", "PORT8", "PORT9"]
            },
            {
                'slug': 'region_3',
                'parent_slug_id': 'region_2',
                'ports': ["POR10"]
            },
            {
                'slug': 'region_eu_1',
                'parent_slug_id': 'region_eu',
                'ports': ["POR11", "POR12", "POR13"]
            },
        ]

        for region in region_dataset:
            region_instance = baker.make(
                Region, slug=region['slug'], parent_slug_id=region['parent_slug_id']
            )

            for port_code in region.get('ports', []):
                baker.make(Port, code=port_code, parent_slug=region_instance)

    def prepare_price_data(self):
        price_dataset = [
            {
                'origin_code': 'PORT3',
                'destination_code': 'PORT4',
                'days': [
                    {
                        'date': "2023-03-15",
                        'prices': [100, 200, 300, 400, 500, 600]
                    },
                    {
                        'date': "2023-03-16",
                        'prices': [100, 200, 300]
                    },
                    {
                        'date': "2023-03-17",
                        'prices': [100, 200, 300, 400, 500]
                    }
                ]
            },
            {
                'origin_code': 'USP3',
                'destination_code': 'PORT4',
                'days': [
                    {
                        'date': "2023-03-15",
                        'prices': [100, 200, 300, 400, 500, 600]
                    },
                    {
                        'date': "2023-03-16",
                        'prices': [100, 200, 300]
                    },
                    {
                        'date': "2023-03-17",
                        'prices': [100, 200, 300, 400, 500]
                    }
                ]
            },
            {
                'origin_code': 'USP4',
                'destination_code': 'PORT7',
                'days': [
                    {
                        'date': "2023-03-15",
                        'prices': [100, 200]
                    },
                    {
                        'date': "2023-03-16",
                        'prices': [100, 200]
                    },
                    {
                        'date': "2023-03-17",
                        'prices': []
                    }
                ]
            },
            {
                'origin_code': 'USP3',
                'destination_code': 'PORT8',
                'days': [
                    {
                        'date': "2023-03-15",
                        'prices': [100, 200]
                    },
                    {
                        'date': "2023-03-16",
                        'prices': [100, 200]
                    },
                    {
                        'date': "2023-03-17",
                        'prices': [100, 200]
                    }
                ]
            },
            {
                'origin_code': 'USP1',
                'destination_code': 'POR10',
                'days': [
                    {
                        'date': "2023-03-15",
                        'prices': [100, 200]
                    },
                    {
                        'date': "2023-03-16",
                        'prices': [100, 200]
                    },
                    {
                        'date': "2023-03-18",
                        'prices': [100, 200, 200, 300]
                    }
                ]
            }
        ]

        for price_data in price_dataset:
            for day_data in price_data.get('days', []):
                for price in day_data.get('prices', []):
                    baker.make(
                        Price, orig_code_id=price_data['origin_code'],
                        dest_code_id=price_data['destination_code'],
                        day=day_data['date'],
                        price=price
                    )

    def setUp(self):
        self.manager = RateCalculatorManager()
        self.prepare_region_data()
        self.prepare_price_data()


    def test_calculate_rate_between_port3_port4(self):
        expected = [
            {
                'day': '2023-03-14',
                'average_price': None,
            },
            {
                'day': '2023-03-15',
                'average_price': 350.00,
            },
            {
                'day': '2023-03-16',
                'average_price': None,
            },
            {
                'day': '2023-03-17',
                'average_price': 300.00,
            },
            {
                'day': '2023-03-18',
                'average_price': None,
            }
        ]
        self.assertEqual(expected, self.manager.calculate_rate(
            origin_port=["PORT3"], destination_port=["PORT4"],
            date_from=datetime(year=2023, month=3, day=14),
            date_to=datetime(year=2023, month=3, day=18)
        ))

    def test_calculate_rate_between_region_eu_region_1(self):
        expected = [
            {
                'day': '2023-03-14',
                'average_price': None,
            },
            {
                'day': '2023-03-15',
                'average_price': 150.00,
            },
            {
                'day': '2023-03-16',
                'average_price': 150.00,
            },
            {
                'day': '2023-03-17',
                'average_price': None,
            },
            {
                'day': '2023-03-18',
                'average_price': 200.00,
            }
        ]

        self.assertEqual(expected, self.manager.calculate_rate(
            origin_port=["USP1", "USP2", "USP3", "USP4"],
            destination_port=["PORT7", "PORT8", "PORT9", "POR10"],
            date_from=datetime(year=2023, month=3, day=14),
            date_to=datetime(year=2023, month=3, day=18)
        ))

