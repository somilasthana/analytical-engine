from singlecard.contract.calcinterface import CalculationInterface

import pandas as pd
import numpy as np


class ComplexMeanCalculation(CalculationInterface):

    def __init__(self, ts: pd.DataFrame=None):
        super().__init__(ts)

    def calculate(self, **field: str):
        self.check()

        metric = None
        other_key = None

        if "metric" in field:
            metric = field.get("metric")

        if "other_key" in field:
            other_key = field.get("other_key")

        if metric in self.data.columns and other_key in self.data.columns:
            comp_df = self.data.groupby(by=other_key).agg({metric: np.mean})
        else:
            raise Exception("field = {0} or {1} doesnt exist in self.data".format(metric, other_key))
        return comp_df



