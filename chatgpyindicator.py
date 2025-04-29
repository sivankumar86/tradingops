import yfinance as yf
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands
from ta.trend import MACD, EMAIndicator, SMAIndicator
from ta.trend import ADXIndicator

from samco_ops import samcoAPI

# Email Configuration
EMAIL = "sivankumar@gmail.com"
PASSWORD = "6535n@vi$"
TO_EMAIL = "recipient_email@gmail.com"


def send_email(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())


def getUSmarket(ticker):
    df = yf.download(ticker, period="200d", interval="1d")
    df.dropna(inplace=True)
    df.reset_index(inplace=True)  # Add date as a column

    df["Date"] = df["Date"].astype(str)  # Ensure Date is string for better readability

    return df
def get_stock_data(df):

    df.columns = ["day","close", "high", "low", "open", "volume"]
    df["RSI"] = RSIIndicator(df["close"].astype(int), window=10).rsi()
    indicator_bb = BollingerBands(df["close"].astype(int), window=18)
    df["BB_Upper"] = indicator_bb.bollinger_hband().astype(float)
    df["BB_Lower"] = indicator_bb.bollinger_lband().astype(float)
    macd = MACD(df["close"].astype(float), window_slow=24, window_fast=10, window_sign=8)
    df["MACD"] = macd.macd().astype(float)
    df["MACD_Signal"] = macd.macd_signal().astype(float)
    df["EMA_50"] = EMAIndicator(df["close"].astype(float), window=40).ema_indicator().astype(float)
    df["EMA_200"] = EMAIndicator(df["close"].astype(float), window=240).ema_indicator().astype(float)
    df["SMA_20"] = SMAIndicator(df["close"].astype(float), window=25).sma_indicator().astype(float)
    df["SMA_100"] = SMAIndicator(df["close"].astype(float), window=80).sma_indicator().astype(float)
    df["Stoch_K"] = StochasticOscillator(df["high"].astype(float), df["low"].astype(float), df["close"].astype(float),
                                         window=14, smooth_window=3).stoch().astype(float)
    df["Volume_Avg_10"] = df["volume"].rolling(window=10).mean()

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

    return df


def check_entry_conditions(ticker,df):
    df = get_stock_data(df)
    last_row = df.iloc[-1]

    conditions = []

    if last_row["RSI"] < 30:
        conditions.append({ "symbol": ticker , "message": f"RSI is oversold at {last_row['RSI']:.2f}"})

    if last_row["close"] <= last_row["BB_Lower"]:
        conditions.append({ "symbol": ticker , "message": f"Price hit lower Bollinger Band at {last_row['close']:.2f}"})

    if last_row["MACD"] > last_row["MACD_Signal"]:
        conditions.append({ "symbol": ticker , "message": "MACD bullish crossover detected"})

    if last_row["close"] > last_row["EMA_50"] and last_row["close"] > last_row["EMA_200"] and (last_row["close"] - ( 0.01 * last_row["close"]))  < last_row["EMA_50"] :
        conditions.append({ "symbol": ticker , "message": f"Price above both EMA 50 and EMA 200 (bullish trend) {last_row['EMA_50']}"})

    if last_row["Stoch_K"] < 20:
        conditions.append({ "symbol": ticker , "message": f"Stochastic Oscillator is oversold at {last_row['Stoch_K']:.2f}"})

    if last_row["close"] > last_row["SMA_20"] and (last_row["close"] - ( 0.01 * last_row["close"]))  < last_row["SMA_20"]:
        conditions.append({"symbol": ticker, "message": f"Price is above SMA 20 (short-term uptrend)"})

    if last_row["close"] < last_row["SMA_100"] and (last_row["close"] + ( 0.01 * last_row["close"]))  > last_row["SMA_100"]:
        conditions.append({"symbol": ticker, "message": f"Price is below SMA 100 (long-term downtrend) {last_row["SMA_100"]}"})

    if last_row["MACD"] < last_row["MACD_Signal"] and abs(last_row["MACD"] - last_row["MACD_Signal"]) < 2:
        conditions.append({"symbol": ticker, "message": "MACD bearish crossover detected"})

    if last_row["RSI"] > 70:
        conditions.append({"symbol": ticker, "message": f"RSI is overbought at {last_row['RSI']:.2f}"})

    if last_row["close"] < last_row["EMA_50"] and (last_row["close"] + ( 0.01 * last_row["close"]))  > last_row["EMA_50"]:
        conditions.append({"symbol": ticker, "message": f"Price dropped below EMA 50 (potential bearish move) {last_row['EMA_50']}"})

    if last_row["close"] > last_row["BB_Upper"]:
        conditions.append({"symbol": ticker, "message": f"Price hit upper Bollinger Band at {last_row['close']:.2f} (potential reversal)"})

    if last_row["Stoch_K"] > 80:
        conditions.append({"symbol": ticker, "message": f"Stochastic Oscillator is overbought at {last_row['Stoch_K']:.2f}"})

    if last_row["volume"] > last_row["Volume_Avg_10"] * 1.5:
        conditions.append({"symbol": ticker, "message": f"({last_row['day']}): Volume spike detected (1.5x average 10-day volume)"})

        if last_row["close"] > last_row["EMA_50"]:
            conditions.append(
                {"symbol": ticker, "message": f"({last_row['day']}): Volume spike with price above EMA 50 (bullish confirmation) {last_row['EMA_50']}"})
        else:
            conditions.append(
                {"symbol": ticker, "message": f"({last_row['day']}): Volume spike with price below EMA 50 (possible panic selling, wait for confirmation)"})

    if (0.01 * last_row["open"]) > abs(((last_row["max_40"] + last_row["min_40"]) / 2) - last_row["close"]) > 80:
        conditions.append(
            {"symbol": ticker, "message":f"({last_row['day']}): Iron Condor possible side ways"})

    if 45 > last_row["rsi"] > last_row["rsi_y"] and last_row["adx"] > 20:
        conditions.append(
            {"symbol": ticker, "message": f"({last_row['day']}): rsi_adx_buy (bullish confirmation)"})

    if last_row["rsi"] > last_row["rsi_y"] and last_row["bb_bbla"] > 0:
        conditions.append(
            {"symbol": ticker, "message": f"({last_row['day']}): bb_buy (bullish confirmation)"})

    if 65 < last_row["rsi"] < last_row["rsi_y"] and last_row["adx"] > 20:
        conditions.append(
            {"symbol": ticker, "message": f"({last_row['day']}): rsi_adx_sell (Bearish/side way confirmation)"})

    if last_row["rsi"] < last_row["rsi_y"] and last_row["bb_bbha"] > 0:
        conditions.append(
            {"symbol": ticker, "message": f"({last_row['day']}): bb_sell (Bearish/side way confirmation)"})

    if 45 > last_row["rsi"] > last_row["rsi_y"] and abs(last_row["width"]) > (0.001 * last_row["open"]) and last_row[
        "tail"] > (2 * abs(last_row["width"])):
        conditions.append(
            {"symbol": ticker, "message": f"({last_row['day']}): candle_buy (bullish confirmation)"})

    return conditions


def us_monitor_market():
    alerts = []
    for ticker in ["SPY", "QQQ", "AMZN", "GOOGL", "NVDA", "XLF", "DIA", "IWM"]:
        conditions = check_entry_conditions(ticker,getUSmarket(ticker))
        if conditions:
            alerts.extend(conditions)

    # if alerts:
    #     df=pd.DataFrame(alerts)
    #     print(df.to_html())
        # send_email("Trading Alert: Entry Signal Detected", message)
        #print("Alert Sent: \n", message)
    return alerts



def india_monitor_market():
    alerts = []
    for symbol in ["NIFTY BANK", "NIFTY 50"]:
        
        from datetime import datetime, timedelta
        # Calculate date 365 days ago
        date_365_days_ago = datetime.today() - timedelta(days=365)

        # Convert to string in ISO format
        fromdate = date_365_days_ago.strftime('%Y-%m-%d')
        sa=samcoAPI()
        request_login = sa.login(requestBody=requestBody)
        session_token = request_login['sessionToken']
        inverselist = sa.getIndexHistory(session_token=session_token, symbol=symbol, fromdate=fromdate)
        df = pd.DataFrame(inverselist["indexCandleData"])
        df = df.drop('ltp', axis=1)
        df["volume"] = pd.to_numeric(df["volume"])
        df["open"] = pd.to_numeric(df["open"])
        df["close"] = pd.to_numeric(df["close"])
        df["high"] = pd.to_numeric(df["high"])
        df["low"] = pd.to_numeric(df["low"])
        conditions = check_entry_conditions(symbol,df)
        if conditions:
            alerts.extend(conditions)

    return alerts




# Start monitoring
us_output=us_monitor_market()
in_output=india_monitor_market()

total=us_output + in_output

df=pd.DataFrame(total)
print(df.to_html())
