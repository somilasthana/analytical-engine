from singlecard.contract.measureinterface import MeasureInterface


class ChartMeasure(MeasureInterface):

    def __init__(self, config):
        super().__init__(config)
        self.chart_params = []

    def measure(self):

        for period_name_value, value in zip(list(self.data.index), list(self.data[self.measure_type])):
            self.chart_params.append({
                "xaxis": period_name_value,
                "dim": "",
                "value": float(value)
            })
        return self.chart_params