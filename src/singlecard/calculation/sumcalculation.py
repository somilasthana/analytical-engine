from singlecard.contract.calcinterface import CalculationInterface

import pandas as pd
import numpy as np


class SumCalculation(CalculationInterface):

    def __init__(self, ts: pd.DataFrame=None):
        super().__init__(ts)

    def calculate(self, **field: str):
        self.check()

        metric = None

        if "metric" in field:
            metric = field.get("metric")

        if metric in self.data.columns:
            agg_val = np.sum(self.data[metric])
        else:
            raise Exception("field = {} doesnt exist in self.data".format(field))
        return agg_val

