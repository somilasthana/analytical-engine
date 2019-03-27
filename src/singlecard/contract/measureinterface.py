import abc
from singlecard.tools.logkeeping import print_me_log


class MeasureInterface:
    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        self.config = config

        if self.config is None:
            print_me_log(statement="BasicMeasure needs config", tag="BasicMeasure")
            raise Exception("Config parameter is None")

        if "measure_type" in self.config:
            self.measure_type = self.config["measure_type"]
        else:
            print_me_log(statement="BasicMeasure needs measure measure_type in config", tag="BasicMeasure")
            raise Exception("measure_type expected but doesnt exist")

        if "data" in self.config:
            self.data = self.config["data"]
        else:
            print_me_log(statement="BasicMeasure expects data in config", tag="BasicMeasure")
            raise Exception("No data field in config")

        if "type_name" in self.config:
            self.type_name = self.config["type_name"]
        else:
            self.type_name = "measure"

    @abc.abstractmethod
    def measure(self):
        pass