from datetime import datetime
from singlecard.singleconstant import GranularityFormat


class Granularity:
    def __init__(self, gran_value):
        self.gran_value = gran_value
    def __call__(self, d):
        return d.strftime(self.gran_value)


class GranularityType:
    def gtype(self, value):
        if value == "monthly":
            return GranularityFormat.MONTHLY.value