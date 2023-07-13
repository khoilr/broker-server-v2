from typing import Union

from talipp import indicators
from talipp.ohlcv import OHLCVFactory


class TechnicalAnalysis:
    def __init__(self, name: str, params: dict[str, Union[int, float, str]]) -> None:
        self.func = getattr(indicators, name)
        self.func = self.func(**params)

    def add_inputs(self, prices: dict, input_values: str) -> None:
        if input_values == "OHLCV":
            ohlcv = OHLCVFactory.from_dict(prices)
            input_values = ohlcv
        else:
            input_values = [float(price[input_values.title()]) for price in prices]

        self.func.add_input_value(input_values)

    def compose(self) -> list[float]:
        return self.func.output_values

    def decompose(self) -> dict[str, list[float]]:
        return self.func.to_lists()

    def get_outputs(self) -> Union[list[float], dict[str, list[float]]]:
        try:
            output = self.decompose()
        except:
            output = self.compose()

        return output
