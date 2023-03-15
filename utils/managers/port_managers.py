import logging

from api.models import Port
from utils.managers.base_manager import BasePRManager

logger = logging.getLogger(__name__)


class PortManager(BasePRManager):

    def get_port_list_by_code(self, port_code):
        return list(Port.objects.values_list('code').get(code=port_code))

