import pandas as pd
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
from ta.trend import ADXIndicator

def extract_technical(df) -> pd:
    df["open"] = pd.to_numeric(df["open"])
    df["close"] = pd.to_numeric(df["close"])
    df["high"] = pd.to_numeric(df["high"])
    df["low"] = pd.to_numeric(df["low"])
    indicator_bb = BollingerBands(close=df["close"], window=20, window_dev=2)
    # Add Bollinger Bands features
    df['bb_bbm'] = indicator_bb.bollinger_mavg()
    df['bb_bbh'] = indicator_bb.bollinger_hband()
    df['bb_bbl'] = indicator_bb.bollinger_lband()
    # Add Bollinger Band high indicator
    df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()
    df['bb_bbha'] = df['bb_bbhi'].rolling(window=3).max()

    # Add Bollinger Band low indicator
    df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()
    df['bb_bbla'] = df['bb_bbli'].rolling(window=3).max()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    df['max_40'] = df['close'].rolling(window=40).max()
    df['min_40'] = df['close'].rolling(window=40).min()
    # Add Width Size Bollinger Bands
    df['bb_bbw'] = indicator_bb.bollinger_wband()
    # Add Percentage Bollinger Bands
    df['bb_bbp'] = indicator_bb.bollinger_pband()
    indicator_rsi = RSIIndicator(close=df["close"], window=15)
    df["rsi"] = indicator_rsi.rsi()
    df["width"] = df.apply(lambda row: row["open"] - row["close"], axis=1)
    df["tail"] = df.apply(lambda row: row["open"] - row["low"] if 0 > row["width"] else row["close"] - row["low"],
                          axis=1)
    df["rsi_y"] = df["rsi"].shift(1)
    indicator_adx = ADXIndicator(close=df["close"], high=df["high"], low=df["low"], window=15)
    df["adx"] = indicator_adx.adx()
    df["iron_condor"] = df.apply(
        lambda row: True if (0.01 * row["open"]) > abs(((row["max_40"] + row["min_40"])/2) - row["close"]) else False,
        axis=1)
    df["rsi_adx_buy"] = df.apply(lambda row: True if 45 > row["rsi"] > row["rsi_y"] and row["adx"] > 20  else False,
                                 axis=1)
    df["bb_buy"] = df.apply(lambda row: True if  row["rsi"] > row["rsi_y"] and row["bb_bbla"] > 0 else False,
                                 axis=1)
    df["rsi_adx_sell"] = df.apply(lambda row: True if 65 < row["rsi"] < row["rsi_y"] and row["adx"] > 20 else False,
                                  axis=1)
    df["bb_sell"] = df.apply(lambda row: True if row["rsi"] < row["rsi_y"] and row["bb_bbha"] > 0  else False,
                                  axis=1)
    df["candle_buy"] = df.apply(
        lambda row: True if 45 > row["rsi"] > row["rsi_y"] and abs(row["width"]) > (0.001 * row["open"]) and row[
            "tail"] > (2 * abs(row["width"])) else False, axis=1)
    return df
