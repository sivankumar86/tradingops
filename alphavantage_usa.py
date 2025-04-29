import requests

def get_usmarket(symbol) -> list:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey=ZDTKYPNCPGY66T6E' #&outputsize=full
    r = requests.get(url)
    data = r.json()
    reformat = []
    for key, value in data["Time Series (Daily)"].items():
        reformat.append({"date": key,
                         "open": value["1. open"],
                         "high": value["2. high"],
                         "low": value["3. low"],
                         "close": value["4. close"]
                         })
    inverselist = reformat[::-1]
    return inverselist