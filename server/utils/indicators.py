from talipp.ohlcv import OHLCVFactory
from talipp import indicators


class TechnicalAnalysis:
    def __init__(self, name: str, kwargs: dict) -> None:
        self.func = getattr(indicators, name)
        self.func = self.func(**kwargs)

    def add_inputs(self, prices: dict, input_type: str):
        if input_type == "OHLCV":
            ohlcv = OHLCVFactory.from_dict(prices)
            input_values = ohlcv
        else:
            input_values = [float(price[input_type.title()]) for price in prices]

        self.func.add_input_value(input_values)

    def compose(self):
        return self.func.output_values

    def decompose(self):
        return self.func.to_lists()

    def get_outputs(self):
        try:
            output = self.decompose()
        except:
            output = self.compose()

        return output
