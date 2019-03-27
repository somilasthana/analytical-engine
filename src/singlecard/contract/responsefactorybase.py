import abc

from singlecard.response.singleresponse import SingleResponse
from singlecard.granularity.granularitydriver import Granularity
from singlecard.granularity.granularitydriver import GranularityType

import pandas as pd


class ResponseFactoryBase:
    __metaclass__ = abc.ABCMeta

    def __init__(self, date_field_name: str, response_name_list: list, granularity_type: str, ts: pd.DataFrame, calculation_type, other_key: str=None):
        self.date_field_name = date_field_name
        self.response_name_list = response_name_list
        self.granularity_type = granularity_type
        self.other_key = other_key
        self.ts = ts
        self.calculation_type = calculation_type
        self.df_group = None
        self.modified_date_field_name = "Time_Granularity"


        if date_field_name is None or ts is None:
            raise Exception("date_field_name or data frame cannot be None")

        if date_field_name not in ts.columns:
            raise Exception("Data Frame doesnt has column {}".format(date_field_name))

        gran_format = GranularityType().gtype(self.granularity_type)
        g = Granularity(gran_format)
        self.ts["Time_Granularity"] = self.ts[self.date_field_name].apply(g)
        self.ts["DateObject"] = pd.to_datetime(self.ts[self.date_field_name])
        self.ts.sort_values(by='DateObject', inplace=True, ascending=True)
        self.ts.drop(["DateObject"], axis=1, inplace=True)
        self.query_builder()

    @abc.abstractmethod
    def query_builder(self):
        pass

    def create_response_object(self, response_name: str):
        return SingleResponse(self.calculation_type, self.modified_date_field_name, response_name, self.df_group)
