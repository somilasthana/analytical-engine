import pandas as pd


class MeasureConfig(pd.Series):
    """
    This class extends Pandas Series for conveniently store key-pair value
    s = State()
    s["param1"] = value1
    s["param2"] = value2
    """
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            super().__init__(list(kwargs.values()), index=kwargs)
        else:
            msg = '__init__() takes no positional argument'
            raise TypeError(msg)


class DriverConfig(MeasureConfig):
    pass