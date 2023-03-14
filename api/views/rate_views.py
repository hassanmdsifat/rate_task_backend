import logging


from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from api.models import Price
from utils.helpers.date_time_helpers import validate_date_params
from utils.managers.port_managers import PortManager

logger = logging.getLogger(__name__)


class RateView(APIView):

    def get(self, request):
        port_manager = PortManager()

        try:
            date_from = request.query_params.get('date_from')
            date_to = request.query_params.get('date_to')
            origin = request.query_params.get('origin')
            destination = request.query_params.get('destination')

            parsed_date_from, parsed_date_to = validate_date_params(date_from, date_to)
            origin_code_type = port_manager.validate_provided_code(origin)
            destination_code_type = port_manager.validate_provided_code(destination)

            origin_port_list = port_manager.get_port_list(origin, origin_code_type)
            destination_port_list = port_manager.get_port_list(destination, destination_code_type)

            return Response(status=HTTP_200_OK)

        except ValidationError as E:
            return Response(
                {
                    'errors': E.detail
                }, status=HTTP_400_BAD_REQUEST)

        except Exception as E:
            logger.error(str(E), exc_info=True)
            return Response(str(E), status=HTTP_500_INTERNAL_SERVER_ERROR)