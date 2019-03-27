from singlecard.driver.singlecarddriver import SingleCardDriver
from singlecard.config.singlecardconfig import DriverConfig


def do_test_driver():
    print("==============do_test_driver=================")
    d = DriverConfig(fpath="/Users/somil/workspace/newsroom/small_supermarket/",
                     granularity_type="monthly",
                     date_field_name="Transaction_Date",
                     response_name_list="Sales"
                     )

    driver = SingleCardDriver(d)
    r = driver.create_single_cards()
    assert len(r) == 1
    result = r[0]
    assert result["response_last"] == 54073.479999998046
    assert result["response_change"] == -20779.24000000181
    assert result["percent_change"] == -0.2776016689841311
    assert result["mean_mom"] == -1364.1200000001938
    assert result["mean_growth"] == -0.006007989247170909
    assert result["std_mom"] == 14373.703068366454
    assert result["count"] == 18


def do_multitest_driver():
    print("==============do_multitest_driver=================")
    d = DriverConfig(fpath="/Users/somil/workspace/newsroom/small_supermarket/",
                     granularity_type="monthly",
                     date_field_name="Transaction_Date",
                     response_name_list="Sales,Qty"
                     )

    driver = SingleCardDriver(d)
    r = driver.create_single_cards()
    assert len(r) == 2

    result = r[0]
    assert result["response_last"] == 54073.479999998046
    assert result["response_change"] == -20779.24000000181
    assert result["percent_change"] == -0.2776016689841311
    assert result["mean_mom"] == -1364.1200000001938
    assert result["mean_growth"] == -0.006007989247170909
    assert result["std_mom"] == 14373.703068366454
    assert result["count"] == 18

    result = r[1]
    assert result["response_last"] == 21059.0
    assert result["response_change"] == -9934.0
    assert result["percent_change"] == -0.3205239892879037
    assert result["mean_mom"] == -555.4705882352941
    assert result["mean_growth"] == -0.004184494796913192
    assert result["std_mom"] == 5980.139641470581
    assert result["count"] == 18


if __name__ == '__main__':
    do_test_driver()
    do_multitest_driver()