from singlecard.contract.measurefactoryinterface import MeasureFactoryInterface
from singlecard.singleconstant import MeasureType
from singlecard.measure.basicmeasure import BasicMeasure
from singlecard.measure.chartmeasure import ChartMeasure
from singlecard.tools.logkeeping import print_me_log


class MeasureFactory(MeasureFactoryInterface):

    def __init__(self):
        pass

    def create_measure_object(self, measure_type, config=None):

        print_me_log(statement="Factory creating a measure instance of {}".format(measure_type),
                     tag="MeasureFactory")

        if measure_type == MeasureType.BASIC_MEASURE.value:
            return BasicMeasure(config)
        elif measure_type == MeasureType.CHART_MEASURE.value:
            return ChartMeasure(config)
        else:
            raise Exception("Unknown Measure Type Requested")

