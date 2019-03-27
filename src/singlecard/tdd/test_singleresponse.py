from singlecard.response.responsefactory import SingleResponseTotalFactory
from singlecard.response.responsefactory import SingleResponseAverageFactory
from singlecard.response.responsefactory import SingleResponseComplexCountingFactory
from singlecard.response.responsefactory import SingleResponseComplexMeanFactory
from singlecard.response.responsefactory import SingleResponseFactorFactory

from singlecard.response.singleresponse import SingleResponse
import pandas as pd
import pyarrow.parquet as pq
from datetime import datetime

def test_single_response():
    print("==============test_single_response=================")
    data = pd.DataFrame(data={"Sales": [1, 2, 3], "TransDate": ["01-01-2019", "01-02-2019", "01-03-2019"]})
    s = SingleResponse(calculation_type="sum", date_field_name="TransDate", ts=data, response_name="Sales")

    result = s.respond()

    assert result is not None
    assert result["response_last"] == 3
    assert result["response_change"] == 1.0
    assert result["percent_change"] == 0.5
    assert result["mean_mom"] == 1.0
    assert result["mean_growth"] == 0.75
    assert result["std_mom"] == 0.0
    assert result["count"] == 3


def test_single_factory_test():
    print("==============test_single_factory_test=================")
    data = pd.DataFrame({"Sales": [1, 2, 3], "Quantity": [10, 20, 30], "TransDate": [ datetime.strptime("2019-01-01", "%Y-%m-%d"),
                                                                                      datetime.strptime("2019-02-01", "%Y-%m-%d"),
                                                                                      datetime.strptime("2019-03-01", "%Y-%m-%d")]})
    s = SingleResponseTotalFactory(date_field_name="TransDate", response_name_list=["Sales", "Quantity"],
                                   granularity_type="monthly", ts=data)

    response = s.create_response_object(response_name="Sales")
    assert response is not None

    response = s.create_response_object(response_name="Quantity")
    result = response.respond()

    assert result is not None
    assert result["response_last"] == 30
    assert result["response_change"] == 10.0
    assert result["percent_change"] == 0.5
    assert result["mean_mom"] == 10.0
    assert result["mean_growth"] == 0.75
    assert result["std_mom"] == 0.0
    assert result["count"] == 3


def test_supermarket_total():
    print("==============test_supermarket_total=================")
    pdata = pq.ParquetDataset("/Users/somil/workspace/newsroom/small_supermarket/")
    table = pdata.read()
    data = table.to_pandas()
    s = SingleResponseTotalFactory(date_field_name="Transaction_Date", response_name_list=["Sales", "Qty"],
                                   granularity_type="monthly", ts=data)
    assert s is not None
    response = s.create_response_object(response_name="Sales")
    result = response.respond()

    assert result is not None

    assert result["response_last"] == 54073.479999998046
    assert result["response_change"] == -20779.24000000181
    assert result["percent_change"] == -0.2776016689841311
    assert result["mean_mom"] == -1364.1200000001938
    assert result["mean_growth"] == -0.006007989247170909
    assert result["std_mom"] == 14373.703068366454
    assert result["count"] == 18


def test_supermarket_mean():
    print("==============test_supermarket_mean=================")
    pdata = pq.ParquetDataset("/Users/somil/workspace/newsroom/small_supermarket/")
    table = pdata.read()
    data = table.to_pandas()
    s = SingleResponseAverageFactory(date_field_name="Transaction_Date", response_name_list=["Sales", "Qty"],
                                   granularity_type="monthly", ts=data)
    assert s is not None
    response = s.create_response_object(response_name="Sales")
    result = response.respond()

    assert result is not None

    assert result["response_last"] == 3.231161039736961
    assert result["response_change"] == 0.08542790252326693
    assert result["percent_change"] == 0.027156754497914548
    assert result["mean_mom"] == -0.004324900344565981
    assert result["mean_growth"] == -0.0007479881084359564
    assert result["std_mom"] == 0.11297239657894537
    assert result["count"] == 18

    response = s.create_response_object(response_name="Qty")
    result = response.respond()


def test_supermarket_complex_count():
    print("==============test_supermarket_complex count=================")
    pdata = pq.ParquetDataset("/Users/somil/workspace/newsroom/small_supermarket/")
    table = pdata.read()
    data = table.to_pandas()

    s = SingleResponseComplexCountingFactory(date_field_name="Transaction_Date", response_name_list=["Sales", "Qty"],
                                   granularity_type="monthly", ts=data, other_key="Customer_Id")

    response = s.create_response_object(response_name="Customer_Id")
    result = response.respond()

    assert result is not None

    assert result["response_last"] == 1320
    assert result["response_change"] == -473.0
    assert result["percent_change"] == -0.2638036809815951
    assert result["mean_mom"] == -54.0
    assert result["mean_growth"] ==  -0.017128494844207264
    assert result["std_mom"] == 358.85733688374563
    assert result["count"] == 18

    s = SingleResponseComplexCountingFactory(date_field_name="Transaction_Date", response_name_list=["Sales", "Qty"],
                                   granularity_type="monthly", ts=data, other_key="Basket_Id")

    response = s.create_response_object(response_name="Basket_Id")
    result = response.respond()

    assert result is not None
    assert result["response_last"] == 1420
    assert result["response_change"] == -586.0
    assert result["percent_change"] == -0.292123629112662
    assert result["mean_mom"] == -69.17647058823529
    assert result["mean_growth"] ==  -0.021290253285595966
    assert result["std_mom"] == 398.36108882950106
    assert result["count"] == 18


def test_supermarket_complex_mean():
    print("==============test_supermarket_complex mean=================")
    pdata = pq.ParquetDataset("/Users/somil/workspace/newsroom/small_supermarket/")
    table = pdata.read()
    data = table.to_pandas()

    s = SingleResponseComplexMeanFactory(date_field_name="Transaction_Date", response_name_list=["Sales", "Qty"],
                                   granularity_type="monthly", ts=data, other_key="Customer_Id")

    response = s.create_response_object(response_name="Sales")
    result = response.respond()

    assert result is not None
    assert result["response_last"] == 40.964757575756096
    assert result["response_change"] == -0.7824370700887755
    assert result["percent_change"] == -0.01874226703677806
    assert result["mean_mom"] == 0.3788994231861643
    assert result["mean_growth"] ==  0.010478388471856578
    assert result["std_mom"] == 1.048810675913787
    assert result["count"] == 18


def test_supermarket_factor():
    print("==============test_supermarket_factor mean=================")
    pdata = pq.ParquetDataset("/Users/somil/workspace/newsroom/small_supermarket/")
    table = pdata.read()
    data = table.to_pandas()

    s = SingleResponseFactorFactory(date_field_name="Transaction_Date", response_name_list=["Sales", "Qty"],
                                   granularity_type="monthly", ts=data, other_key="Age_Band")

    response = s.create_response_object(response_name="55-64")
    result = response.respond()

    assert result is not None
    assert result["response_last"] == 3.5166841798014774
    assert result["response_change"] == 0.18526076939686398
    assert result["percent_change"] == 0.055610094117205966
    assert result["mean_mom"] == -0.024852890824320708
    assert result["mean_growth"] ==  -0.001642670594694277
    assert result["std_mom"] == 0.36160959531986553
    assert result["count"] == 18


if __name__ == '__main__':
    test_single_response()
    test_single_factory_test()
    test_supermarket_total()
    test_supermarket_mean()
    test_supermarket_complex_count()
    test_supermarket_complex_mean()
    test_supermarket_factor()
