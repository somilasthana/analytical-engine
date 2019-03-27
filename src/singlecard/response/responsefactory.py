from singlecard.contract.responsefactorybase import ResponseFactoryBase
from singlecard.singleconstant import SingleResponseType

import pandas as pd
import numpy as np


class SingleResponseTotalFactory(ResponseFactoryBase):

    def __init__(self, date_field_name: str, response_name_list: list, granularity_type: str, ts: pd.DataFrame):
        super().__init__(date_field_name, response_name_list, granularity_type, ts, SingleResponseType.SINGLE_TOTAL_RESPONSE.value)

    def query_builder(self):
        agg_map = {k: np.sum for k in self.response_name_list}
        self.df_group = self.ts.groupby([self.modified_date_field_name], sort=False).agg(agg_map).reset_index()


class SingleResponseAverageFactory(ResponseFactoryBase):

    def __init__(self, date_field_name: str, response_name_list: list, granularity_type: str, ts: pd.DataFrame):
        super().__init__(date_field_name, response_name_list, granularity_type, ts, SingleResponseType.SINGLE_AVG_RESPONSE.value)

    def query_builder(self):
        agg_map = {k: np.mean for k in self.response_name_list}
        self.df_group = self.ts.groupby([self.modified_date_field_name], sort=False).agg(agg_map).reset_index()


class SingleResponseComplexCountingFactory(ResponseFactoryBase):

    def __init__(self, date_field_name: str, response_name_list: list, granularity_type: str, ts: pd.DataFrame, other_key: str):
        super().__init__(date_field_name, response_name_list, granularity_type, ts, SingleResponseType.SINGLE_TOTAL_RESPONSE.value, other_key)

    def query_builder(self):
        self.df_group = self.ts.groupby([self.modified_date_field_name], sort=False)[self.other_key].agg(list).reset_index()
        self.df_group[self.other_key] = self.df_group[self.other_key].apply(lambda x: len(set(x)))


class SingleResponseComplexMeanFactory(ResponseFactoryBase):

    def __init__(self, date_field_name: str, response_name_list: list, granularity_type: str, ts: pd.DataFrame, other_key: str):
        super().__init__(date_field_name, response_name_list, granularity_type, ts, SingleResponseType.SINGLE_TOTAL_RESPONSE.value, other_key)

    def query_builder(self):
        df_group_unique = self.ts.groupby([self.modified_date_field_name], sort=False)[self.other_key].agg(list).reset_index()
        df_group_unique[self.other_key] = df_group_unique[self.other_key].apply(lambda x: len(set(x)))

        agg_map = {k: np.sum for k in self.response_name_list}
        self.df_group = self.ts.groupby([self.modified_date_field_name], sort=False).agg(agg_map).reset_index()

        self.df_group =  self.df_group.merge(df_group_unique, on=self.modified_date_field_name)
        for k in self.response_name_list:
            self.df_group[k] = self.df_group[k] / self.df_group[self.other_key]


class SingleResponseFactorFactory(ResponseFactoryBase):

    def __init__(self, date_field_name: str, response_name_list: list, granularity_type: str, ts: pd.DataFrame, other_key: str):
        super().__init__(date_field_name, response_name_list, granularity_type, ts, SingleResponseType.SINGLE_TOTAL_RESPONSE.value, other_key)

    def query_builder(self):
        response_column_name = self.response_name_list[0]
        self.df_group = self.ts.pivot_table(index=self.modified_date_field_name, columns=self.other_key,
                                             values=response_column_name, aggfunc=np.mean)

        self.df_group = self.df_group.reset_index()

