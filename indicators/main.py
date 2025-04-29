
import pandas as pd
from technical import extract_technical
from alphavantage_usa import get_usmarket
from samco_ops import login,getIndexHistory

def analysis(df,symbol):
    ldf = df.tail(1)
    rsi_buy = ldf["rsi_adx_buy"].item()
    rsi_sell = ldf["rsi_adx_sell"].item()
    c_buy = ldf["candle_buy"].item()
    iron = ldf["iron_condor"].item()

    day = ldf["date"].item()
    if rsi_buy or c_buy:
        return {"symbol": symbol, "day": day, "comments": "rsi : " + str(rsi_buy) + "c_buy : " + str(c_buy), "recommend": "buy"}
    elif rsi_sell:
        return {"symbol": symbol, "day": day, "comments": "rsi : " + str(rsi_sell), "recommend": "sell"}
    elif iron:
        max = ldf["max_40"].item()
        min = ldf["min_40"].item()
        open = ldf["open"].item()
        return {"symbol": symbol, "day": day, "comments": "iron_condor : min {} max {} open {}".format(min,max,open), "recommend": "iron condor"}
    return None


result=[]
for symbol in ["SPY","QQQ","VXX","AMZN","NVDA","META","GOOG","AAPL"]:
    try:
        inverselist=get_usmarket(symbol)
        df = pd.DataFrame(inverselist)
        df = extract_technical(df)
        temp_res=analysis(df,symbol)
        if temp_res:
            result.append(temp_res)
    except Exception as e:
        print( "error : "+str(e))


print("US Results : ")
print(result)
requestBody={
  "userId": "RR38403",
  "password": "Dhruvan@0606",
  "yob": "1965"
}
fromdate='2022-10-11'
request_login=login(requestBody)
session_token=request_login['sessionToken']


for symbol in ["NIFTY BANK","NIFTY 50"]:
    inverselist=getIndexHistory(session_token,symbol,fromdate)
    df = pd.DataFrame(inverselist["indexCandleData"])
    df = extract_technical(df)
    temp_res=analysis(df,symbol)
    if temp_res:
        result.append(temp_res)




def send_email_details(output):
    import boto3
    client = boto3.client(
        'ses',
        region_name="ap-southeast-2"
    )
    response = client.send_email(
        Destination={
            'ToAddresses': ['sivankumar86@gmail.com'],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': output.to_html(),
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Stock Analysis',
            },
        },
        Source='sivankumar86@gmail.com',
    )
    print(response)


if len(result) > 0:
    output=pd.DataFrame(result)
    print(result)
    send_email_details(output)