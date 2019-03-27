from singlecard.contract.calcfactoryinterface import CalculationFactoryInterface
from singlecard.singleconstant import CalcType
from singlecard.calculation.sumcalculation import SumCalculation
from singlecard.calculation.meancalculation import MeanCalculation
from singlecard.calculation.stdcalculation import StdCalculation
from singlecard.calculation.countcalculation import CountCalculation
from singlecard.calculation.complexcountcalculation import ComplexCountCalculation
from singlecard.calculation.complexmeancalculation import ComplexMeanCalculation
from singlecard.calculation.complexsumcalculation import ComplexSumCalculation
from singlecard.calculation.complexmaxcalculation import ComplexMaxCalculation

from utils.syslog_util import print_me_log


class CalculationFactory(CalculationFactoryInterface):

    def __init__(self):
        pass

    def create_calc_object(self, cal_type, ts=None):

        print_me_log(statement="Factory creating a calculation instance of {}".format(cal_type), tag="CalculationFactory")

        if cal_type == CalcType.COUNT_CALCULATION.value:
            return CountCalculation(ts)
        elif cal_type == CalcType.SUM_CALCULATION.value:
            return SumCalculation(ts)
        elif cal_type == CalcType.MEAN_CALCULATION.value:
            return MeanCalculation(ts)
        elif cal_type == CalcType.STANDARD_DEV_CALCULATION.value:
            return StdCalculation(ts)
        elif cal_type == CalcType.COMPLEX_COUNT_CALCULATION.value:
            return ComplexCountCalculation(ts)
        elif cal_type == CalcType.COMPLEX_MEAN_CALCULATION.value:
            return ComplexMeanCalculation(ts)
        elif cal_type == CalcType.COMPLEX_SUM_CALCULATION.value:
            return ComplexSumCalculation(ts)
        elif cal_type == CalcType.COMPLEX_MAX_CALCULATION.value:
            return ComplexMaxCalculation(ts)
        else:
            raise Exception("Unknown Calculation Type Requested")