from singlecard.measure.derivedmeasuresinglenews import DerivedMeasureSingleCard
from singlecard.config.singlecardconfig import MeasureConfig
import pandas as pd


def test_singlecard_errcase():
    print("==============test_singlecard_errcase=================")
    try:
        d = DerivedMeasureSingleCard(None)
    except Exception as e:
        assert str(e) == "Config parameter is None"


def test_singlecard_news():
    print("==============test_singlecard_news=================")

    mconfig = MeasureConfig(measure_type="Sales",
                            data=pd.DataFrame(data={"Sales": [1,2,3]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                                               ))

    d = DerivedMeasureSingleCard(mconfig)
    f = d.measure()

    assert f["mean_mom"] == 1.0
    assert f["mean_growth"] == 0.75
    assert f["std_mom"] == 0.0
    assert f["count"] == 3


if __name__ == '__main__':
    test_singlecard_errcase()
    test_singlecard_news()