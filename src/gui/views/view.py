from abc import ABC, abstractmethod

class View(ABC):

    @abstractmethod
    def set_controller(self):
        pass
