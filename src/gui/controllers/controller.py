from abc import ABC, abstractmethod

class Controller(ABC):

    def __init__(self, view):
        self.view = view
