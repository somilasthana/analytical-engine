from singlecard.response.responsefactory import SingleResponseTotalFactory
from singlecard.granularity.granularitydriver import Granularity
from singlecard.granularity.granularitydriver import GranularityType
from singlecard.tools.readdata import ReadDataParquet
from singlecard.news.singlecardgenerator import SingleCardGenerator

import pandas as pd


class SingleCardDriver:

    def __init__(self, config):
        self.df = ReadDataParquet().read_to_df(config.fpath)
        self.granularity_type = config.granularity_type
        self.date_field_name = config.date_field_name
        self.response_name_list = config.response_name_list.split(",")

        self.total_response = SingleResponseTotalFactory(date_field_name=self.date_field_name,
                                                         response_name_list = self.response_name_list,
                                                         granularity_type = self.granularity_type,
                                                         ts=self.df)
        self.response_object = {}

        for resp_name in self.response_name_list:
            self.response_object.setdefault(resp_name, self.total_response.create_response_object(response_name=resp_name))

    def create_single_cards(self):
        resultlist = []
        for resp_name in self.response_name_list:
            resultlist.append(self.response_object[resp_name].respond())
        return resultlist

