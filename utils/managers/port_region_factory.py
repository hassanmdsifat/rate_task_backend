from utils.managers.port_managers import PortManager
from utils.managers.region_manager import RegionManager


class PortRegionFactory:

    def __init__(self):
        self.factory = {
            'port': PortManager(),
            'region': RegionManager(),
        }

    def get_manager_by_code(self, code):
        return self.factory[code]