import pyarrow.parquet as pq
from singlecard.contract.readdatainterface import ReadDataInterface


class ReadDataParquet(ReadDataInterface):

    def __init__(self):
        pass

    def read_to_df(self, fpath):
        dataset = pq.ParquetDataset(fpath)
        table = dataset.read()
        df = table.to_pandas()
        return df
