from singlecard.contract.derivedmeasureinterface import DerivedMeasureInterface
from singlecard.tools.logkeeping import print_me_log
from singlecard.config.singlecardconfig import MeasureConfig
from singlecard.measure.measurefactory import MeasureFactory
from singlecard.singleconstant import CalcType
from singlecard.singleconstant import MeasureType

import pandas as pd


class DerivedMeasureSingleCard(DerivedMeasureInterface):

    def __init__(self, config):
        super().__init__(config)
        self.basic_measure_list = {}
        self._process()

    def _process(self):
        """
        Internal function - basic_measure_list could be a list as well, made a dict for readabiilty
        :return:
        """

        self.basic_measure_list.setdefault("response_last", self.response())
        self.basic_measure_list.setdefault("response_change", self.response_change())
        self.basic_measure_list.setdefault("percent_change", self.response_pct_change())
        self.basic_measure_list.setdefault("mean_mom", self.mean_mom())
        self.basic_measure_list.setdefault("mean_growth", self.mean_growth())
        self.basic_measure_list.setdefault("std_mom", self.std_mom())
        self.basic_measure_list.setdefault("count_mom", self.count())

    def response(self):
        return {"response_last": self.data.iloc[-1][self.measure_type]}

    def response_change(self):

        diff_data = self.data[self.measure_type].diff()
        diff_data.dropna(inplace=True)
        return {"response_change": diff_data.iloc[-1]}

    def response_pct_change(self):

        pct_data = self.data[self.measure_type].pct_change()
        pct_data.dropna(inplace=True)
        return {"percent_change": pct_data.iloc[-1]}

    def mean_mom(self):

        diff_series = self.data[self.measure_type].diff()
        diff_data = pd.DataFrame(index=self.data.index, data={self.measure_type: diff_series})
        diff_data.dropna(inplace=True)

        measure_config = MeasureConfig(measure_type=self.config["measure_type"], data=diff_data, type_name="mean_mom",
                                       calculation_type=CalcType.MEAN_CALCULATION.value)

        diff_measure_object = MeasureFactory().create_measure_object(MeasureType.BASIC_MEASURE.value, measure_config)

        return diff_measure_object.measure()

    def mean_growth(self):

        pct_series = self.data[self.measure_type].pct_change()
        pct_data = pd.DataFrame(index=self.data.index, data={self.measure_type: pct_series})
        pct_data.dropna(inplace=True)

        measure_config = MeasureConfig(measure_type=self.config["measure_type"], data=pct_data, type_name="mean_growth",
                                       calculation_type=CalcType.MEAN_CALCULATION.value)

        pct_measure_object = MeasureFactory().create_measure_object(MeasureType.BASIC_MEASURE.value, measure_config)

        return pct_measure_object.measure()

    def std_mom(self):

        diff_series = self.data[self.measure_type].diff()
        diff_data = pd.DataFrame(index=self.data.index, data={self.measure_type: diff_series})
        diff_data.dropna(inplace=True)

        measure_config = MeasureConfig(measure_type=self.config["measure_type"], data=diff_data, type_name="std_mom",
                                       calculation_type=CalcType.STANDARD_DEV_CALCULATION.value)

        diff_measure_object = MeasureFactory().create_measure_object(MeasureType.BASIC_MEASURE.value, measure_config)

        return diff_measure_object.measure()

    def count(self):

        measure_config = MeasureConfig(measure_type=self.config["measure_type"], data=self.data, type_name="count",
                                       calculation_type=CalcType.COUNT_CALCULATION.value)

        diff_measure_object = MeasureFactory().create_measure_object(MeasureType.BASIC_MEASURE.value, measure_config)

        return diff_measure_object.measure()

    def measure(self):
        result = {}
        for key_type in self.basic_measure_list.keys():
            result.update(self.basic_measure_list[key_type])

        return result
