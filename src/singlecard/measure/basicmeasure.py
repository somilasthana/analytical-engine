from singlecard.contract.measureinterface import MeasureInterface
from singlecard.tools.logkeeping import print_me_log
from singlecard.calculation.calcfactory import CalculationFactory
from singlecard.singleconstant import CalcType


class BasicMeasure(MeasureInterface):

    def __init__(self, config):
        super().__init__(config)
        self.calculation_type = None
        self.chart_params = []

        if "calculation_type" in self.config:
            self.calculation_type = self.config["calculation_type"]
            print_me_log(statement="BasicMeasure uses calculation_type {}".format(self.calculation_type),
                         tag="BasicMeasure")
        else:
            print_me_log(statement="BasicMeasure doesnt has any calculation_type set defaulting to SUM",
                         tag="BasicMeasure")

    def measure(self):
        calc_object = CalculationFactory().create_calc_object(cal_type=self.calculation_type if self.calculation_type else CalcType.SUM_CALCULATION.value,
                                                                   ts=self.data)

        cal_result = calc_object.calculate(metric=self.measure_type)

        return {self.type_name: cal_result}


