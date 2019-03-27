import abc


class MeasureFactoryInterface:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_measure_object(self, measure_type, config):
        pass
