import pandas as pd
import pyarrow.parquet as pq
import numpy as np

from datetime import datetime
from sklearn.linear_model import LinearRegression

from singlecard.granularity.granularitydriver import Granularity
from singlecard.granularity.granularitydriver import GranularityType

critical_value = [ .0, .997, .950, .878, .811, .754, .707, .666, .632, .602, .576, .553,
  .532, .514, .497, .482, .468, .456, .444, .433, .423, .413, .404, .396,
  .388, .381, .374, .367, .361, .355, .349, .325, .304, .288, .273, .250,
  .232, .217, .205, .195 ]


def test_response_sum_dummy():
    pdata = pq.ParquetDataset("/Users/somil/workspace/newsroom/small_supermarket/")
    table = pdata.read()
    data = table.to_pandas()
    granularity_type = "monthly"
    gran_format = GranularityType().gtype(granularity_type)
    date_field_name = "Transaction_Date"
    g = Granularity(gran_format)
    sdata = data[["Sales", "Qty", "Transaction_Date"]]
    sdata["Time_Granularity"] = sdata[date_field_name].apply(g)

    sdata["DateObject"] = pd.to_datetime(sdata["Time_Granularity"])
    sdata.sort_values(by='DateObject', inplace=True, ascending=True)
    sdata.drop(["DateObject"], axis=1, inplace=True)
    sdata.drop(["Transaction_Date"], axis=1, inplace=True)

    agg_map = {k: np.sum for k in ["Sales", "Qty"]}
    sdata_group = sdata.groupby(["Time_Granularity"], sort=False).agg(agg_map).reset_index()

    sdata_group.loc[(sdata_group['Qty'] == 0), 'Qty'] = 1

    sdata_group["Sales_by_Qty"] = sdata_group["Sales"] / sdata_group["Qty"]

    sdata_diff = pd.DataFrame(data={"Sales": sdata_group["Sales"].diff(),
                                    "Qty": sdata_group["Qty"].diff(),
                                    "Sales_by_Quantity": sdata_group["Sales_by_Qty"].diff()
                                    })
    sdata_diff.dropna(axis=0)



    correlation_value = np.corrcoef(sdata_diff["Sales"], sdata_diff["Qty"])[0, 1]
    sign_records = len(sdata_diff) - 2

    if correlation_value > critical_value[sign_records]:
        print("Sales Qty related")


def test_response_elasticity_dummy():
    pdata = pq.ParquetDataset("/Users/somil/workspace/newsroom/small_supermarket/")
    table = pdata.read()
    data = table.to_pandas()
    granularity_type = "monthly"
    gran_format = GranularityType().gtype(granularity_type)
    date_field_name = "Transaction_Date"
    g = Granularity(gran_format)
    sdata = data[["Sales", "Qty", "Transaction_Date"]]
    sdata["Time_Granularity"] = sdata[date_field_name].apply(g)

    sdata["DateObject"] = pd.to_datetime(sdata["Time_Granularity"])
    sdata.sort_values(by='DateObject', inplace=True, ascending=True)
    sdata.drop(["DateObject"], axis=1, inplace=True)
    sdata.drop(["Transaction_Date"], axis=1, inplace=True)

    agg_map = {k: np.sum for k in ["Sales", "Qty"]}
    sdata_elastic = sdata.groupby(["Time_Granularity"], sort=False).agg(agg_map).reset_index()

    sdata_elastic_model = pd.DataFrame(data={"DiffSales": sdata_elastic["Sales"].diff(),
                                    "DiffQty": sdata_elastic["Qty"].diff(),
                                    "RollingSales": sdata_elastic['Sales'].rolling(2).sum(),
                                    "RollingQty": sdata_elastic['Qty'].rolling(2).sum()
                                    })
    sdata_elastic_model.dropna(axis=0, inplace=True)

    sdata_elastic_model["Elastic_Quantity_Elasticity"] = (sdata_elastic_model["DiffQty"] / sdata_elastic_model["RollingQty"]) \
                                                         / (sdata_elastic_model["DiffSales"] / sdata_elastic_model["RollingSales"])


def test_response_mean_dummy():
    pdata = pq.ParquetDataset("/Users/somil/workspace/newsroom/small_supermarket/")
    table = pdata.read()
    data = table.to_pandas()
    granularity_type = "monthly"
    gran_format = GranularityType().gtype(granularity_type)
    date_field_name = "Transaction_Date"
    g = Granularity(gran_format)
    sdata = data[["Sales", "Qty", "Transaction_Date"]]
    sdata["Time_Granularity"] = sdata[date_field_name].apply(g)

    sdata["DateObject"] = pd.to_datetime(sdata["Time_Granularity"])
    sdata.sort_values(by='DateObject', inplace=True, ascending=True)
    sdata.drop(["DateObject"], axis=1, inplace=True)
    sdata.drop(["Transaction_Date"], axis=1, inplace=True)

    agg_map = {k: np.mean for k in ["Sales", "Qty"]}
    sdata.drop(["Transaction_Date"], axis=1, inplace=True)

    sdata_group = sdata.groupby(["Time_Granularity"], sort=False).agg(agg_map).reset_index()

    sdata_group.loc[(sdata_group['Qty'] == 0), 'Qty'] = 1

    sdata_group["Sales_by_Qty"] = sdata_group["Sales"] / sdata_group["Qty"]

    sdata_diff = pd.DataFrame(data={"Sales": sdata_group["Sales"].diff(),
                                    "Qty": sdata_group["Qty"].diff(),
                                    "Sales_by_Quantity": sdata_group["Sales_by_Qty"].diff()
                                    })
    sdata_diff.dropna(axis=0, inplace=True)

    correlation_value = np.corrcoef(sdata_diff["Sales"], sdata_diff["Qty"])[0, 1]
    sign_records = len(sdata_diff) - 2

    if correlation_value > critical_value[sign_records]:
        print("Sales Qty related")

def test_complex_count_dummy():
    pdata = pq.ParquetDataset("/Users/somil/workspace/newsroom/small_supermarket/")
    table = pdata.read()
    data = table.to_pandas()
    granularity_type = "monthly"
    gran_format = GranularityType().gtype(granularity_type)
    date_field_name = "Transaction_Date"
    g = Granularity(gran_format)
    complex_calc_data = data[["Basket_Id", "Customer_Id", "Product_Id", "Transaction_Date", "Sales"]]
    complex_calc_data["Time_Granularity"] = complex_calc_data[date_field_name].apply(g)

    complex_calc_data["DateObject"] = pd.to_datetime(complex_calc_data[date_field_name])
    complex_calc_data.sort_values(by='DateObject', inplace=True, ascending=True)
    complex_calc_data.drop(["DateObject"], axis=1, inplace=True)
    complex_calc_data.drop(["Transaction_Date"], axis=1, inplace=True)

    complex_calc_data_group = complex_calc_data.groupby(["Time_Granularity"], sort=False).agg(list).reset_index()

    complex_calc_data_group["Complex_Customer_Id"] = complex_calc_data_group["Customer_Id"].apply(
        (lambda x: len(set(x))))
    complex_calc_data_group["Complex_Product_Id"] = complex_calc_data_group["Product_Id"].apply((lambda x: len(set(x))))
    complex_calc_data_group["Complex_Basket_Id"] = complex_calc_data_group["Basket_Id"].apply((lambda x: len(set(x))))

    complex_calc_data_group["Total_Sales"] = complex_calc_data_group["Sales"].apply((lambda x: sum(x)))

    complex_calc_data_group["Complex_Mean_Customer_Id"] = complex_calc_data_group["Total_Sales"] / \
                                                          complex_calc_data_group["Complex_Customer_Id"]

    complex_calc_data_group["Complex_Mean_Product_Id"] = complex_calc_data_group["Total_Sales"] / \
                                                         complex_calc_data_group["Complex_Product_Id"]

    complex_calc_data_group["Complex_Mean_Basket_Id"] = complex_calc_data_group["Total_Sales"] / \
                                                        complex_calc_data_group["Complex_Basket_Id"]

    complex_calc_data_diff = pd.DataFrame(data={"Basket_Id": complex_calc_data_group["Complex_Basket_Id"].diff(),
                                                "Customer_Id": complex_calc_data_group["Complex_Customer_Id"].diff(),
                                                "Product_Id": complex_calc_data_group["Complex_Product_Id"].diff()})

    complex_calc_data_diff.dropna(axis=0, inplace=True)

    np.corrcoef(complex_calc_data_diff["Basket_Id"], complex_calc_data_diff["Customer_Id"])

    np.corrcoef(complex_calc_data_diff["Basket_Id"], complex_calc_data_diff["Product_Id"])

    np.corrcoef(complex_calc_data_diff["Customer_Id"], complex_calc_data_diff["Product_Id"])

    """"
    data_diff = pd.DataFrame(data={"Basket_Id": complex_calc_data_group["Complex_Basket_Id"].diff(),
                                   "Customer_Id": complex_calc_data_group["Complex_Customer_Id"].diff(),
                                   "Product_Id": complex_calc_data_group["Complex_Product_Id"].diff(),
                                   "Sales": sdata_group["Sales"].diff(), "Qty": sdata_group["Qty"].diff(),
                                   "Sales_by_Quantity": sdata_group["Sales_by_Qty"].diff(),
                                   "Mean_Basket_Id": complex_calc_data_group["Complex_Mean_Basket_Id"].diff(),
                                   "Mean_Customer_Id": complex_calc_data_group["Complex_Mean_Customer_Id"].diff(),
                                   "Mean_Product_Id": complex_calc_data_group["Complex_Mean_Product_Id"].diff()})
                                   
    data_diff.to_csv("/Users/somil/Documents/Kaggle/SingleCardEngine/analytical-engine/src/measure.csv")
                                   
    norm_data_diff=(data_diff-data_diff.min())/(data_diff.max()-data_diff.min())
    

def getlinear(x,y):
 
    def inner(x1):
        return m * x1 + b
    
    m = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) * np.sum(x))
    b = (np.sum(y) - m *np.sum(x)) / len(x)
    return inner
    
    
    def sigmoid(x, derivative=False):
        sigm = 1. / (1. + np.exp(-x))
        if derivative:
            return sigm * (1. - sigm)
        return sigm
    cmap = {}
    for column_name in list(norm_data_diff.columns):
        y = norm_data_diff[column_name].values
        X = np.array(range(1,len(norm_data_diff) + 1)).reshape(-1, 1)
        reg = LinearRegression().fit(X, y)
        score = reg.score(X, y)
        pred = reg.predict([[18]])
        print("{0}: {1}".format(column_name, reg.coef_[0]))
        cmap.setdefault(column_name, reg.coef_[0])
        
    for k,v in sorted(cmap, key = lambda x: x[1]):
        print("{0}: {1}", k, v)
    
    """

    def travel_age():
        start = datetime.now()
        pdata = pq.ParquetDataset("/tmp/traveledge")
        table = pdata.read()
        data = table.to_pandas()
        end = datetime.now()
        feature_data = data[
            ["CO2_tons", "advance_purchase", "bookings_with_hotel_attached", "days_away", "hotel_room_nights_attached",
             "kilometres", "lost_savings", "miles", "room_nights", "room_nights_leakage", "spend", "spend_NZD", "spend_including_GST",
             "spend_including_GST_NZD", "supplier_rate_AUD", "supplier_rate_NZD", "tickets", "bookings", "hotels",
             "booked_date", "flights"]]

        date_field_name = "booked_date"
        """
        MONTHLY = "%b-%Y"
        class Granularity:
            def __init__(self, gran_value):
                self.gran_value = gran_value
            def __call__(self, d):
                return d.strftime(self.gran_value)

        g = Granularity(MONTHLY)
        """

        feature_data["Time_Granularity"] = feature_data[date_field_name].apply(g)

        feature_data["DateObject"] = pd.to_datetime(feature_data["Time_Granularity"])

        feature_data.sort_values(by='DateObject', inplace=True, ascending=True)

        feature_data.drop(["DateObject"], axis=1, inplace=True)
        feature_data.drop([date_field_name], axis=1, inplace=True)

        sum_data = feature_data[
            ["CO2_tons", "hotel_room_nights_attached", "bookings_with_hotel_attached", "kilometres", "miles", "flights",
             "lost_savings", "room_nights", "room_nights_leakage", "spend", "spend_NZD", "spend_including_GST",
             "spend_including_GST_NZD", "supplier_rate_AUD", "supplier_rate_NZD", "tickets", "Time_Granularity"]]

        clist = list(sum_data.columns)
        clist.remove("Time_Granularity")

        agg_map = {k: np.sum for k in clist}

        sum_data_group = sum_data.groupby(["Time_Granularity"], sort=False).agg(agg_map).reset_index()

        param = { column_name: sum_data_group[column_name].diff() for column_name in clist}

        sum_data_diff = pd.DataFrame(data=param)

        sum_data_diff.dropna(axis=0, inplace=True)

        sum_data_diff.to_csv("~/spark-warehouse/traveledge_sum.csv")

        norm_sum_data_diff = (sum_data_diff - sum_data_diff.min()) / (sum_data_diff.max() - sum_data_diff.min())

        for column_name in list(norm_sum_data_diff.columns):
            norm_sum_data_diff.loc[(norm_sum_data_diff[column_name] < 0.5), column_name] = 0

        v = norm_sum_data_diff.astype(bool).sum(axis=0)
        v.sort_values(ascending=False)
        """
        tickets                         31
        miles                           31
        kilometres                      31
        CO2_tons                        31
        supplier_rate_NZD               30
        spend_including_GST_NZD         30
        supplier_rate_AUD               29
        spend_including_GST             29
        spend                           29
        bookings_with_hotel_attached    29
        hotel_room_nights_attached      25
        lost_savings                    21
        room_nights_leakage             14
        room_nights                     11                        
        """

        cmap = {}
        for column_name in list(norm_sum_data_diff.columns):
            y = norm_sum_data_diff[column_name].values
            X = np.array(range(1, len(norm_sum_data_diff) + 1)).reshape(-1, 1)
            reg = LinearRegression().fit(X, y)
            print("{0}: {1}".format(column_name, reg.coef_[0]))
            cmap.setdefault(column_name, reg.coef_[0])

        """
        bookings_with_hotel_attached:-0.008516667649258606
        spend:-0.007632999833021594
        spend_including_GST:-0.007583665826860517
        supplier_rate_AUD:-0.00750832511784103
        tickets:-0.007030248041497061
        spend_including_GST_NZD:-0.00573449091429419
        supplier_rate_NZD:-0.0056618590995920854
        CO2_tons:-0.004252087488905791
        kilometres:-0.004201677794866936
        miles:-0.004201677794866646
        hotel_room_nights_attached:-0.003080742765017798
        lost_savings:-0.0018344211556681478
        room_nights_leakage:0.003809131098794359
        room_nights:0.011657931842759053
        """

        complex_data = feature_data[
            ['bookings', 'CO2_tons', 'spend', 'spend_NZD' , 'spend_including_GST', 'spend_including_GST_NZD',
             'lost_savings','advance_purchase', 'days_away', 'hotel_room_nights_attached', 'room_nights',
             'supplier_rate_AUD', 'supplier_rate_NZD', 'advance_purchase' ,'hotels', 'Time_Granularity']]

        complex_data_group = complex_data.groupby(["Time_Granularity"], sort=False).agg(list).reset_index()

        complex_data_group["unique_bookings_count"] = complex_data_group["bookings"].apply(
            (lambda x: len(set(x))))

        complex_data_group["unique_hotels_booking_count"] = complex_data_group["hotels"].apply(
            (lambda x: len(set(x))))

        complex_data_group["Total_CO2"] = complex_data_group["CO2_tons"].apply((lambda x: sum(x)))
        complex_data_group["Complex_Mean_CO2_tons"] = complex_data_group["Total_CO2"] / \
                                                         complex_data_group["unique_bookings_count"]

        for column_name in ['CO2_tons','advance_purchase', 'days_away', 'hotel_room_nights_attached', 'supplier_rate_AUD', 'supplier_rate_NZD']:
            complex_data_group["Total_" + column_name] = complex_data_group[column_name].apply((lambda x: sum(x)))
            complex_data_group["Complex_Mean_" + column_name] = complex_data_group["Total_" + column_name] / \
                                                      complex_data_group["unique_bookings_count"]

        for column_name in ['CO2_tons', 'supplier_rate_AUD', 'supplier_rate_NZD', 'lost_savings', 'advance_purchase']:
            complex_data_group["mean_" + column_name + "_per_unique_booking"] = mean_data_group[column_name] / complex_data_group["unique_bookings_count"]

        for column_name in ['days_away', 'advance_purchase']:
            complex_data_group["total_" + column_name + "_per_unique_booking"] = sum_data_group[column_name] / complex_data_group["unique_bookings_count"]

        for column_name in ['room_nights', 'spend', 'spend_NZD' , 'spend_including_GST', 'spend_including_GST_NZD']:
            complex_data_group["Total_" + column_name] = complex_data_group[column_name].apply((lambda x: sum(x)))
            complex_data_group["Complex_Mean_" + column_name] = complex_data_group["Total_" + column_name] / \
                                                                complex_data_group["unique_bookings_count"]
            complex_data_group["Complex_Mean_" + column_name] = complex_data_group["Total_" + column_name] / \
                                                                complex_data_group["unique_hotels_booking_count"]

        for column_name in ['room_nights', 'spend', 'spend_including_GST']:
            complex_data_group["mean_" + column_name + "_per_unique_booking"] = mean_data_group[column_name] / complex_data_group["unique_bookings_count"]
            complex_data_group["mean_" + column_name + "_per_unique_hotel_booking"] = mean_data_group[column_name] / complex_data_group["unique_hotels_booking_count"]

        clist = ["Unique_bookings", "Unique_hotels", "Complex_Mean_CO2_tons", "Complex_Mean_advance_purchase",
                 "Complex_Mean_days_away", "Complex_Mean_hotel_room_nights_attached", "Complex_Mean_room_nights"]
        param = {column_name: complex_data_group[column_name].diff() for column_name in clist}
        complex_data_diff = pd.DataFrame(data=param)

        complex_data_diff.dropna(axis=0, inplace=True)

        complex_data_diff.to_csv("~/spark-warehouse/traveledge_complex.csv")

        norm_complex_data_diff = (complex_data_diff - complex_data_diff.min()) / (complex_data_diff.max() - complex_data_diff.min())

        for column_name in list(norm_complex_data_diff.columns):
            norm_complex_data_diff.loc[(norm_complex_data_diff[column_name] < 0.5), column_name] = 0

        v = norm_complex_data_diff.astype(bool).sum(axis=0)
        v.sort_values(ascending=False)

        """
        Unique_hotels                              33
        Complex_Mean_hotel_room_nights_attached    32
        Unique_bookings                            31
        Complex_Mean_days_away                     25
        Complex_Mean_advance_purchase              20
        Complex_Mean_room_nights                   17
        Complex_Mean_CO2_tons                      10
        """

        cmap = {}
        for column_name in list(norm_complex_data_diff.columns):
            y = norm_complex_data_diff[column_name].values
            X = np.array(range(1, len(norm_complex_data_diff) + 1)).reshape(-1, 1)
            reg = LinearRegression().fit(X, y)
            print("{0}: {1}".format(column_name, reg.coef_[0]))
            cmap.setdefault(column_name, reg.coef_[0])

        """
        Unique_bookings, -0.006045626531902774
        Unique_hotels, -0.005361009590531654
        Complex_Mean_hotel_room_nights_attached, -0.0005963105857115606
        Complex_Mean_advance_purchase, 0.000128775773261101
        Complex_Mean_days_away, 0.0006751587214992609
        Complex_Mean_CO2_tons, 0.001054144368155676
        Complex_Mean_room_nights, 0.009318691051612663
        """


def test_correlation():
    data = pd.read_csv("~/spark-warehouse/traveledge_sum.csv")
    data.drop(['Unnamed: 0'], inplace=True)

    cdata = pd.read_csv("~/spark-warehouse/traveledge_complex.csv")

    final_data = pd.concat([data, cdata], axis=1)
    final_data = (final_data - final_data.min()) / (final_data.max() - final_data.min())

    corr_array = np.corrcoef(final_data)

    corr_array[corr_array < 0.482] = 0

    edge = {}

    for ind, feature_name in enumerate(final_data.columns):
        for corr in corr_array[ind]:
            if corr == 0 or corr == 1:
                continue
            if corr < 0.482 and corr > -0.482:
                continue
            edge.setdefault(feature_name, 0)
            edge[feature_name] += 1



    for key in sorted(edge, key=edge.get):
        print("{0}: {1}".format(key, edge[key]))





def logic3(feature_data):
    from sklearn.linear_model import LinearRegression
    sum_data = feature_data[
        ["CO2_tons", "hotel_room_nights_attached", "bookings_with_hotel_attached", "kilometres", "miles",
         "lost_savings", "room_nights", "room_nights_leakage", "spend", "spend_including_GST",
         "spend_including_GST_NZD", "supplier_rate_AUD", "supplier_rate_NZD", "tickets", "Time_Granularity"]]
    start = datetime.now()
    clist = list(sum_data.columns)
    clist.remove("Time_Granularity")
    agg_map = {k: np.sum for k in clist}
    sum_data_group = sum_data.groupby(["Time_Granularity"], sort=False).agg(agg_map).reset_index()
    print("Len {0}".format(len(sum_data_group)))
    param = {column_name: sum_data_group[column_name].diff() for column_name in clist}
    sum_data_diff = pd.DataFrame(data=param)
    sum_data_diff.dropna(axis=0, inplace=True)
    norm_sum_data_diff = (sum_data_diff - sum_data_diff.min()) / (sum_data_diff.max() - sum_data_diff.min())
    corr_array = np.corrcoef(norm_sum_data_diff)
    corr_array[corr_array < 0.482] = 0
    edge = {}
    for ind, feature_name in enumerate(norm_sum_data_diff.columns):
        for corr in corr_array[ind]:
            if corr == 0 or corr == 1:
                continue
            if corr < 0.482 and corr > -0.482:
                continue
            edge.setdefault(feature_name, 0)
            edge[feature_name] += 1
    print(edge)
    end = datetime.now()
    return end-start












