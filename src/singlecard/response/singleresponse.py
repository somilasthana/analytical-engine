from singlecard.contract.responseinterface import SingleResponseInterface
from singlecard.measure.derivedmeasuresinglenews import DerivedMeasureSingleCard
from singlecard.config.singlecardconfig import MeasureConfig

import pandas as pd


class SingleResponse(SingleResponseInterface):

    def __init__(self,  calculation_type: str, date_field_name: str, response_name: str, ts: pd.DataFrame):
        self.calculation_type = calculation_type
        self.date_column = date_field_name
        self.measure_type = response_name
        self.single_derived_card = None
        self.data = None
        self._set_derived_measure(ts)

    def _set_derived_measure(self, ts: pd.DataFrame):
        self.data = self._reset_index(ts, self.date_column)
        mconfig = MeasureConfig(measure_type=self.measure_type, data=self.data)
        self.single_derived_card = DerivedMeasureSingleCard(mconfig)

    @staticmethod
    def _reset_index(ts: pd.DataFrame, date_column: str):
        ts = ts.set_index(date_column)
        return ts

    def respond(self):
        insight = self.single_derived_card.measure()
        return insight

