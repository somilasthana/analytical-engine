from singlecard.calculation.calcfactory import CalculationFactory
import pandas as pd


def test_calculationfactory():
    print("================== Testing test_calculationfactory() =================")

    cf = CalculationFactory()

    try:
        cf.create_calc_object(None, None)
        assert False
    except Exception:
        assert True

    try:
        cf.create_calc_object(None)
        assert False
    except Exception:
        assert True

    try:
        sum_calculation = cf.create_calc_object("sum_calculation")
        assert False
    except Exception:
        assert True


def test_sum_calculation():
    print("================== Testing test_sum_calculation() =================")
    cf = CalculationFactory()

    data = pd.DataFrame(data={"Sales": [1, 2, 3]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                        )
    sum_calc = cf.create_calc_object("sum_calculation")

    sum_calc.assign(data)
    assert sum_calc.calculate(metric="Sales") == 6


def test_mean_calculation():
    print("================== Testing test_mean_calculation() =================")
    cf = CalculationFactory()

    data = pd.DataFrame(data={"Sales": [1, 2, 3]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                        )

    mean_calc = cf.create_calc_object("mean_calculation")
    mean_calc.assign(data)
    assert mean_calc.calculate(metric="Sales") == 2.0


def test_std_calculation():
    print("================== Testing test_mean_calculation() =================")
    cf = CalculationFactory()

    data = pd.DataFrame(data={"Sales": [1, 2, 3]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                        )

    mean_calc = cf.create_calc_object("standard_dev_calculation")
    mean_calc.assign(data)
    assert mean_calc.calculate(metric="Sales") == 0.816496580927726


def test_count_calculation():
    print("================== Testing test_mean_calculation() =================")
    cf = CalculationFactory()

    data = pd.DataFrame(data={"Sales": [1, 2, 3]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                        )

    mean_calc = cf.create_calc_object("count_calculation")
    mean_calc.assign(data)
    assert mean_calc.calculate(metric="Sales") == 3


def test_complex_count_calculation():
    print("================== Testing test_complex_count_calculation() =================")
    cf = CalculationFactory()

    data = pd.DataFrame(data={"Sales": [1, 2, 3], "Prod": ["A", "B", "B"]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                        )

    mean_calc = cf.create_calc_object("complex_count_calculation")
    mean_calc.assign(data)
    df = mean_calc.calculate(metric="Sales", other_key="Prod")

    assert df is not None
    assert df.loc["A"]["Sales"] == 1
    assert df.loc["B"]["Sales"] == 2


def test_complex_mean_calculation():
    print("================== Testing test_complex_mean_calculation() =================")
    cf = CalculationFactory()

    data = pd.DataFrame(data={"Sales": [1, 2, 3], "Prod": ["A", "B", "B"]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                        )

    mean_calc = cf.create_calc_object("complex_mean_calculation")
    mean_calc.assign(data)
    df = mean_calc.calculate(metric="Sales", other_key="Prod")

    assert df is not None
    assert df.loc["A"]["Sales"] == 1.0
    assert df.loc["B"]["Sales"] == 2.5



def test_complex_sum_calculation():
    print("================== Testing test_complex_sum_calculation() =================")
    cf = CalculationFactory()

    data = pd.DataFrame(data={"Sales": [1, 2, 3], "Prod": ["A", "B", "B"]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                        )

    mean_calc = cf.create_calc_object("complex_sum_calculation")
    mean_calc.assign(data)
    df = mean_calc.calculate(metric="Sales", other_key="Prod")

    assert df is not None
    assert df.loc["A"]["Sales"] == 1
    assert df.loc["B"]["Sales"] == 5


def test_complex_max_calculation():
    print("================== Testing test_complex_max_calculation() =================")
    cf = CalculationFactory()

    data = pd.DataFrame(data={"Sales": [1, 2, 3], "Prod": ["A", "B", "B"]}, index=["Jan 2019", "Feb 2019", "Mar 2019"]
                        )

    mean_calc = cf.create_calc_object("complex_max_calculation")
    mean_calc.assign(data)
    df = mean_calc.calculate(metric="Sales", other_key="Prod")

    assert df is not None
    assert df.loc["A"]["Sales"] == 1
    assert df.loc["B"]["Sales"] == 3


if __name__ == '__main__':
    test_calculationfactory()
    test_sum_calculation()
    test_mean_calculation()
    test_std_calculation()
    test_count_calculation()
    test_complex_count_calculation()
    test_complex_mean_calculation()
    test_complex_sum_calculation()
    test_complex_max_calculation()
