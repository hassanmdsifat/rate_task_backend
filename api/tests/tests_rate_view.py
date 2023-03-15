from unittest import mock

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from utils.managers.port_manager import PortManager
from utils.managers.port_region_factory import PortRegionFactory


class TestRateView(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.base_url = reverse('get-rates')

    def test_rate_api_view_without_param_data(self):
        request = self.client.get(path=self.base_url)
        self.assertEqual(400, request.status_code)

    def test_rate_api_view_with_wrong_date(self):
        base_url = "{}?date_from=2023-03-20&date_to=2023-111-20".format(self.base_url)
        request = self.client.get(path=base_url)
        self.assertEqual(400, request.status_code)

    def test_rate_api_view_without_orig_dest(self):
        base_url = "{}?date_from=2023-03-20&date_to=2023-03-24".format(self.base_url)
        request = self.client.get(path=base_url)
        self.assertEqual(400, request.status_code)

    @mock.patch.object(PortManager, 'get_port_list_by_code')
    @mock.patch.object(PortRegionFactory, 'get_manager_by_code')
    @mock.patch('api.views.rate_views.RateCalculatorManager.calculate_rate')
    @mock.patch('api.views.rate_views.ValidatorManager.validate_provided_code')
    @mock.patch('api.views.rate_views.ValidatorManager.validate_date_params')
    def test_rate_api_view_success(
            self,
            mock_validate_date_params,
            mock_validate_provided_code,
            mock_calculate_rate,
            mock_get_manager_by_code,
            mock_get_port_list_by_code
    ):
        mock_validate_date_params.return_value = (True, True)
        mock_validate_provided_code.return_value = "PORT"
        mock_get_manager_by_code.return_value = PortManager()
        mock_get_port_list_by_code.return_value = ["TEST"]
        mock_calculate_rate.return_value = {}

        base_url = "{}?date_from=2023-03-20&date_to=2023-03-24".format(self.base_url)
        request = self.client.get(path=base_url)
        self.assertEqual(200, request.status_code)

    @mock.patch.object(PortManager, 'get_port_list_by_code')
    @mock.patch.object(PortRegionFactory, 'get_manager_by_code')
    @mock.patch('api.views.rate_views.ValidatorManager.validate_provided_code')
    @mock.patch('api.views.rate_views.ValidatorManager.validate_date_params')
    def test_rate_api_view_exception(
            self,
            mock_validate_date_params,
            mock_validate_provided_code,
            mock_get_manager_by_code,
            mock_get_port_list_by_code
    ):
        mock_validate_date_params.return_value = (True, True)
        mock_validate_provided_code.return_value = "PORT"
        mock_get_manager_by_code.return_value = PortManager()
        mock_get_port_list_by_code.return_value = "Unexpected value"

        base_url = "{}?date_from=2023-03-20&date_to=2023-03-24".format(self.base_url)
        request = self.client.get(path=base_url)
        self.assertEqual(500, request.status_code)