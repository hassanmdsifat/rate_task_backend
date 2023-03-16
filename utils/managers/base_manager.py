from abc import ABC, abstractmethod


class BasePRManager(ABC):

    @abstractmethod
    def get_port_list_by_code(self, code):
        pass