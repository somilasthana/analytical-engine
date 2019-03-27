import abc


class ReadDataInterface:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read_to_df(self, fpath):
        pass
