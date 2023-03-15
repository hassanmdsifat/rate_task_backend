import logging

from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from utils.managers.port_manager import PortManager
from utils.managers.port_region_factory import PortRegionFactory
from utils.managers.rate_calculator_manager import RateCalculatorManager
from utils.managers.validation_manager import ValidatorManager

logger = logging.getLogger(__name__)


class RateView(APIView):

    def get(self, request):
        validator_manager = ValidatorManager()
        manager_getter = PortRegionFactory()
        rate_manager = RateCalculatorManager()

        try:
            date_from = request.query_params.get('date_from')
            date_to = request.query_params.get('date_to')
            origin = request.query_params.get('origin')
            destination = request.query_params.get('destination')

            parsed_date_from, parsed_date_to = validator_manager.validate_date_params(
                date_from, date_to
            )
            origin_code_type = validator_manager.validate_provided_code(origin)
            destination_code_type = validator_manager.validate_provided_code(destination)

            """
                GET proper manager from PortRegionFactory
                based on code_type
                and get list of ports 
            """
            origin_port_list = manager_getter.get_manager_by_code(
                origin_code_type
            ).get_port_list_by_code(origin)

            destination_port_list = manager_getter.get_manager_by_code(
                destination_code_type
            ).get_port_list_by_code(destination)

            rate_list = rate_manager.calculate_rate(
                origin_port_list, destination_port_list, parsed_date_from, parsed_date_to
            )

            return Response(data=rate_list, status=HTTP_200_OK)

        except ValidationError as E:
            return Response(
                {
                    'errors': E.detail
                }, status=HTTP_400_BAD_REQUEST)

        except Exception as E:
            logger.error(str(E), exc_info=True)
            return Response(str(E), status=HTTP_500_INTERNAL_SERVER_ERROR)