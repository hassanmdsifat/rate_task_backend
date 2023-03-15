from django.test import TestCase

from model_bakery import baker

from api.models.regions import Region
from api.models.ports import Port
from utils.managers.region_manager import RegionManager


class TestRegionManager(TestCase):

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

    def prepare_test_dataset(self):
        return [
            {
                'slug': 'region_a',
                'expected': ["PORT1", "PORT2", "PORT3", "PORT4", "PORT5", "PORT6"]
            },
            {
                'slug': 'region_b',
                'expected': ["PORT1", "PORT2", "PORT3"]
            },
            {
                'slug': 'region_d',
                'expected': ["PORT5", "PORT6"]
            },
            {
                'slug': 'region_1',
                'expected': ["PORT7", "PORT8", "PORT9", "POR10"]
            },
            {
                'slug': 'region_3',
                'expected': ["POR10"]
            },
            {
                'slug': 'region_us',
                'expected': ["USP1", "USP2", "USP3", "USP4"]
            },
            {
                'slug': 'not_a_valid_slug',
                'expected': [],
            }
        ]

    def setUp(self):
        self.manager = RegionManager()
        self.prepare_region_data()
        self.test_dataset = self.prepare_test_dataset()

    def test_get_port_list_by_code(self):

        for test_data in self.test_dataset:
            self.assertEqual(
                test_data['expected'],
                self.manager.get_port_list_by_code(test_data['slug'])
            )
