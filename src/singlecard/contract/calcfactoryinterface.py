import abc


class CalculationFactoryInterface:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_calc_object(self, cal_type, ts):
        pass
