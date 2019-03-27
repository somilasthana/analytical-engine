import abc
import pandas as pd


class CalculationInterface:
    __metaclass__ = abc.ABCMeta

    def __init__(self, ts: pd.DataFrame=None):
        self.data = ts

    def check(self):
        if self.data is None:
            raise Exception ("No data available to perform calculation")

    def assign(self, data: pd.DataFrame):
        self.data = data

    @abc.abstractmethod
    def calculate(self, **field: str):
        pass