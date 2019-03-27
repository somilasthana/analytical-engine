from enum import Enum


class CalcType(Enum):
    COUNT_CALCULATION = "count_calculation"
    SUM_CALCULATION = "sum_calculation"
    MEAN_CALCULATION = "mean_calculation"
    COMPLEX_COUNT_CALCULATION = "complex_count_calculation"
    COMPLEX_MEAN_CALCULATION = "complex_mean_calculation"
    COMPLEX_SUM_CALCULATION = "complex_sum_calculation"
    COMPLEX_MAX_CALCULATION = "complex_max_calculation"
    GROUP_MEAN_CALCULATION = "group_mean_calculation"
    EXPECTED_MEAN_CALCULATION = "expected_mean_calculation"
    LINEAR_CALCULATION = "linear_mean_calculation"
    INTERVAL_CALCULATION = "interval_calculation"
    STANDARD_DEV_CALCULATION = "standard_dev_calculation"


class MeasureType(Enum):
    BASIC_MEASURE = "basic_measure"
    DERIVED_MEASURE = "derived_measure"
    CHART_MEASURE = "chart_measure"


class SingleResponseType(Enum):
    SINGLE_TOTAL_RESPONSE = "sum"
    SINGLE_AVG_RESPONSE = "mean"


class GranularityFormat(Enum):
    MONTHLY = "%b-%Y"