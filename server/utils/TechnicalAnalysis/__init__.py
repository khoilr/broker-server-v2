"""Initualize module."""
from typing import Union

from talipp import indicators
from talipp.ohlcv import OHLCVFactory


class TechnicalAnalysis:
    """Class for technical analysis creating."""

    def __init__(self, name: str, params: dict[str, Union[int, float, str]]) -> None:
        """
        Initilize object.

        Args:
            name (str): Get indicator name
            params (dict[str, Union[int, float, str]]): Parameter dictionary
        """
        self.func = getattr(indicators, name)
        self.func = self.func(**params)

    def add_inputs(self, prices: list[dict], input_values: str) -> None:
        """
        Add inputs.

        Args:
            prices (list[dict]): List of prices
            input_values (str): Type of input values
        """
        if input_values == "OHLCV":
            input_valuess = [
                [
                    price["Open"],
                    price["High"],
                    price["Low"],
                    price["Close"],
                    price["Volume"],
                ]
                for price in prices
            ]
            input_valuess = OHLCVFactory.from_matrix(input_valuess)
        else:
            input_valuess = [float(price[input_values.title()]) for price in prices]

        self.func.add_input_value(input_valuess)

    def compose(self) -> list[float]:
        """
        Compose TA object.

        Returns:
            list[float]: TA list
        """
        return self.func.output_values

    def decompose(self) -> dict[str, list[float]]:
        """
        Decompose TA object.

        Returns:
            dict[str, list[float]]: TA dict
        """
        return self.func.to_lists()

    def get_outputs(self) -> Union[list[float], dict[str, list[float]]]:
        """
        Get outputs.

        Returns:
            Union[list[float], dict[str, list[float]]]: No idea.
        """
        try:
            output = self.decompose()
        except Exception:
            output = self.compose()

        return output
