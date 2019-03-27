from singlecard.measure.measurefactory import MeasureFactory
from singlecard.config.singlecardconfig import MeasureConfig
import pandas as pd


def test_measurefactory_errcase():
    print("==============test_measurefactory_errcase=================")
    mf = MeasureFactory()

    try:
        mf.create_measure_object(None, None)
        assert False
    except Exception as e:
        assert str(e) == "Unknown Measure Type Requested"

    try:
        mf.create_measure_object("unknown")
        assert False
    except Exception as e:
        assert str(e) == "Unknown Measure Type Requested"

    try:
        measure_handle = mf.create_measure_object("basic_measure")
        assert False
    except Exception as e:
        assert str(e) == "Config parameter is None"


def test_chart_measure():
    print("==============test_chart_measure=================")

    mconfig = MeasureConfig(measure_type="Sales",
                            data=pd.DataFrame(data={"Sales": [1,2,3]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                                               ))
    mf = MeasureFactory()

    measure_handle = mf.create_measure_object("chart_measure", mconfig)

    chart = measure_handle.measure()

    assert 'xaxis' in chart[0]
    assert 'dim' in chart[0]
    assert 'value' in chart[0]

    assert 'Jan 2019' == chart[0]['xaxis']
    assert '' == chart[0]['dim']
    assert 1.0 == chart[0]['value']

    assert 'Feb 2019' == chart[1]['xaxis']
    assert '' == chart[1]['dim']
    assert 2.0 == chart[1]['value']


def test_sum_measure():
    print("==============test_sum_measure=================")

    mconfig = MeasureConfig(measure_type="Sales",
                            data=pd.DataFrame(data={"Sales": [1,2,3]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                                               ))
    mf = MeasureFactory()

    measure_handle = mf.create_measure_object("basic_measure", mconfig)

    value = measure_handle.measure()["measure"]
    assert value == 6


def test_mean_measure():
    print("==============test_mean_measure=================")

    mconfig = MeasureConfig(measure_type="Sales", calculation_type="mean_calculation",
                            data=pd.DataFrame(data={"Sales": [1,2,3]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                                               ))
    mf = MeasureFactory()

    measure_handle = mf.create_measure_object("basic_measure", mconfig)

    value = measure_handle.measure()["measure"]
    assert value == 2.0


def test_count_measure():
    print("==============test_mean_measure=================")

    mconfig = MeasureConfig(measure_type="Sales", calculation_type="count_calculation",
                            data=pd.DataFrame(data={"Sales": [1,2,3]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                                               ))
    mf = MeasureFactory()

    measure_handle = mf.create_measure_object("basic_measure", mconfig)

    value = measure_handle.measure()["measure"]
    assert value == 3


def test_std_measure():
    print("==============test_mean_measure=================")

    mconfig = MeasureConfig(measure_type="Sales", calculation_type="standard_dev_calculation",
                            data=pd.DataFrame(data={"Sales": [1,2,3]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                                               ))
    mf = MeasureFactory()

    measure_handle = mf.create_measure_object("basic_measure", mconfig)

    value = measure_handle.measure()["measure"]
    assert "{:.2f}".format(value) == "0.82"


if __name__ == '__main__':
    test_measurefactory_errcase()
    test_chart_measure()
    test_sum_measure()
    test_mean_measure()
    test_count_measure()
    test_std_measure()