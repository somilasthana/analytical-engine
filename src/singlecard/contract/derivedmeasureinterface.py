import abc
from singlecard.contract.measureinterface import MeasureInterface


class DerivedMeasureInterface(MeasureInterface):
    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        super().__init__(config)

    @abc.abstractmethod
    def measure(self):
        pass


