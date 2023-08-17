import sys
from datetime import datetime, timedelta

import joblib
import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends

from server.utils.ssi.DataClient import DataClient
from server.web.api.predict.schema import PredictInputDTO, PredictOutputDTO

sys.path.append("e:\\Stock\\broker-server-v2")

router = APIRouter()


@router.get("/", response_model=PredictOutputDTO)
async def return_prob(Input: PredictInputDTO = Depends()):
    result_day, result_week = main(Input.symbol)
    response = {
        "symbol": Input.symbol,
        "probability_day": round(result_day, 4),
        "probability_week": round(result_week, 4),
    }
    return response


def create_df(symbol: str = "VN30") -> pd.DataFrame:
    """
    Create dataframe from SSI DataClient

    Args:
        symbol (str, optional): Symbol name. Defaults to "VN30".

    Returns:
        pd.DataFrame: Price data frame
    """
    market_data_client = DataClient()

    # to have at least 22 record for the 21 days MA
    now = datetime.now()
    previous_two_month = now - timedelta(days=70)

    # request data
    data = market_data_client.daily_ohlc(
        symbol=symbol,
        from_date=previous_two_month.strftime(
            "%d/%m/%Y",
        ),  # Change to string with desired data type
        to_date=now.strftime("%d/%m/%Y"),
        page_index=1,
        page_size=100,
    )["data"]
    df = pd.DataFrame(data)
    return df


def calculate_df(df: pd.DataFrame, day: int = 1) -> pd.DataFrame:
    """
    Create Technical Analysis that can improve the performance of modell

    Args:
        day (int): number of day of prediction
        df (pd.DataFrame): Stock dataframe, with ["Close","Volume","Open","High","low"] and "Date" index

    Returns:
        pd.DataFrame: _description_
    """
    # the result from API is str (I have no idea why?), so convert it back to float
    df["High"] = pd.to_numeric(df["High"])
    df["Low"] = pd.to_numeric(df["Low"])
    df["Close"] = pd.to_numeric(df["Close"])
    df["Open"] = pd.to_numeric(df["Open"])
    df["Volume"] = pd.to_numeric(df["Volume"])

    # Calculate H-L (Stock High minus Low price)
    df["H-L"] = df["High"] - df["Low"]

    # Calculate O-C (Stock Close minus Open price)
    df["O-C"] = df["Close"] - df["Open"]

    # Calculate 7 DAYS MA (Stock price's seven days moving average)
    df["7 DAYS MA"] = df["Close"].rolling(window=7).mean()

    # Calculate 14 DAYS MA (Stock price's fourteen days moving average)
    df["14 DAYS MA"] = df["Close"].rolling(window=14).mean()

    # Calculate 21 DAYS MA (Stock price's twenty one days moving average)
    df["21 DAYS MA"] = df["Close"].rolling(window=21).mean()

    # Calculate 28 DAYS MA (Stock price's twenty eight days moving average)
    df["28 DAYS MA"] = df["Close"].rolling(window=28).mean()

    # Calculate 7 DAYS STD DEV (Stock price's standard deviation for the past seven days)
    df["7 DAYS STD DEV"] = df["Close"].rolling(window=7).std()

    df["PreviousPrice"] = df["Close"].shift(1)

    df["Price Change"] = df["Close"].diff()

    # Calculate the positive and negative price changes
    df["Positive Change"] = np.where(df["Price Change"] > 0, df["Price Change"], 0)
    df["Negative Change"] = np.where(
        df["Price Change"] < 0,
        np.abs(df["Price Change"]),
        0,
    )

    period = 14
    df["Average Gain"] = df["Positive Change"].rolling(window=period).mean()
    df["Average Loss"] = df["Negative Change"].rolling(window=period).mean()

    # Calculate the relative strength (RS)
    df["RS"] = df["Average Gain"] / df["Average Loss"]

    df["EMA"] = df["Close"].ewm(span=period, adjust=False).mean()

    # Calculate the RSI
    df["RSI"] = 100 - (100 / (1 + df["RS"]))

    window = 20  # Number of periods for the moving average
    std_dev = 2  # Number of standard deviations for the bands

    # Calculate the middle band (20-day simple moving average)
    df["Middle Band"] = df["Close"].rolling(window=window).mean()

    # Calculate the standard deviation of the closing prices
    df["Standard Deviation"] = df["Close"].rolling(window=window).std()

    # Calculate the upper band (Middle Band + (2 * Standard Deviation))
    df["Upper Band"] = df["Middle Band"] + (std_dev * df["Standard Deviation"])

    # Calculate the lower band (Middle Band - (2 * Standard Deviation))
    df["Lower Band"] = df["Middle Band"] - (std_dev * df["Standard Deviation"])
    df["NextDayChange"] = df["Close"].shift(-day) - df["Close"]

    # Target class, 1 is increase, and 0 is decrease
    df["TargetClass"] = [1 if df.NextDayChange[i] > 0 else 0 for i in range(len(df))]
    # Get only the columns that can help the model perform better
    input_columns = [
        "H-L",
        "O-C",
        "7 DAYS MA",
        "14 DAYS MA",
        "21 DAYS MA",
        "7 DAYS STD DEV",
        "RSI",
        "EMA",
        "Middle Band",
        "Upper Band",
        "Lower Band",
        "Positive Change",
        "Negative Change",
        "Average Gain",
    ]

    return df[input_columns].tail(1)


def predict(df: pd.DataFrame, symbol: str, day) -> float:
    """
    Calculate the probability of stock price increasement

    Args:
        df (pd.DataFrame): Dataframe of stock index, with these columns
        >>> input_columns = ['H-L','O-C','7 DAYS MA','14 DAYS MA','21 DAYS MA','7 DAYS STD DEV', "RSI",'EMA','Middle Band','Upper Band','Lower Band','Positive Change','Negative Change','Average Gain']

        symbol (str): stock symbol

    Returns:
        float: The probability of stock price increasement
    """
    # transform the data
    if day == 1:
        model = joblib.load(open(f"./server/web/api/predict/model/{symbol}.sav", "rb"))
    else:
        model = joblib.load(
            open(f"./server/web/api/predict/model/{symbol}_week.sav", "rb"),
        )
    # predict data
    prediction = model.predict_proba(df)

    probability = float(prediction[:, 1:])
    return probability


def main(symbol):
    df = create_df(symbol=symbol)
    df = (
        df.rename(columns={"TradingDate": "Date"})
        .set_index("Date")
        .drop(columns=["Symbol", "Market", "Time", "Value"])
    )
    df_day = calculate_df(df, 1)
    df_week = calculate_df(df, 7)
    result_day = predict(df_day, symbol, 1)
    result_week = predict(df_week, symbol, 7)
    return result_day, result_week


if __name__ == "__main__":
    result = main("VCB")
    print(result)
