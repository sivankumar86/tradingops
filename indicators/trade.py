from samco_ops import login, getQuote, placeOrder



requestBody={
  "userId": "DR42012",
  "password": "Dhruvan@0606",
  "yob": "1985"
}
fromdate='2022-10-11'
request_login=login(requestBody)
print(request_login)
session_token=request_login['sessionToken']


import requests
headers = {
  'Accept': 'application/json',
  'x-session-token': session_token
}
## "NIFTY BANK","NIFTY 50"
r = requests.get('https://api.stocknote.com/quote/indexQuote', params={
  'indexName': 'NIFTY BANK'
}, headers = headers)

output=r.json()
spotprice=int(float(output['spotPrice']))
remainder=spotprice % 500
number_needtoadd=500-remainder
round_spot=number_needtoadd+spotprice

from datetime import datetime , timedelta

todayDT = datetime.today()+timedelta(days=45)
currentMonth = todayDT.month

nWed = todayDT
while todayDT.month == currentMonth:
    todayDT += timedelta(days=1)
    if todayDT.weekday()==2: #this is Wednesday
        nWed = todayDT
print (nWed)

# import requests
# headers = {
#   'Accept': 'application/json',
#   'x-session-token': session_token
# }
#
# r = requests.get('https://api.stocknote.com/option/optionChain', params={
#   'searchSymbolName': 'BANKNIFTY',"exchange":"NFO","expiryDate":"2024-08-28"
# }, headers = headers)
#
# print(r.json())

trade_pos="PE"
if trade_pos=="CE":
    start="BANKNIFTY{}{}CE".format(nWed.strftime("%y%b"),round_spot)
    end="BANKNIFTY{}{}CE".format(nWed.strftime("%y%b"),round_spot+500)
    print(start)
    print(end)
    start_quote= getQuote(session_token,start)
    end_quote= getQuote(session_token,end)
    start_diff=float(start_quote['bestBids'][0]['price']) - float(start_quote['bestAsks'][0]['price'])
    end_diff=float(end_quote['bestBids'][0]['price']) - float(end_quote['bestAsks'][0]['price'])
    if abs(start_diff) < 10 and abs(end_diff) < 10:
        print(start_quote)
        print(end_quote)
        start_requestBody = {
            "symbolName": start,
            "exchange": "NFO",
            "transactionType": "SELL",
            "orderType": "L",
            "quantity": "15",
            "disclosedQuantity": "15",
            "price": start_quote['bestBids'][0]['price'],
            "priceType": "LTP",
            "marketProtection": "1%",
            "orderValidity": "DAY",
            "afterMarketOrderFlag": "NO",
            "productType": "NRML",
            "triggerPrice": "0.00"
        }
        end_requestBody = {
            "symbolName": end,
            "exchange": "NFO",
            "transactionType": "BUY",
            "orderType": "L",
            "quantity": "15",
            "disclosedQuantity": "15",
            "price": end_quote['bestAsks'][0]['price'],
            "priceType": "LTP",
            "marketProtection": "1%",
            "orderValidity": "DAY",
            "afterMarketOrderFlag": "NO",
            "productType": "NRML",
            "triggerPrice": "0.00"
        }
        startout=placeOrder(session_token,start_requestBody)
        print(startout)
        endout = placeOrder(session_token, end_requestBody)
        print(endout)
else:
    start = "BANKNIFTY{}{}PE".format(nWed.strftime("%y%b"), round_spot)
    end = "BANKNIFTY{}{}PE".format(nWed.strftime("%y%b"), round_spot - 500)
    print(start)
    print(end)
    start_quote = getQuote(session_token, start)
    end_quote = getQuote(session_token, end)
    start_diff = float(start_quote['bestBids'][0]['price']) - float(start_quote['bestAsks'][0]['price'])
    end_diff = float(end_quote['bestBids'][0]['price']) - float(end_quote['bestAsks'][0]['price'])
    print(start_diff)
    print(end_diff)
    if abs(start_diff) < 10 and abs(end_diff) < 10:
        print(start_quote)
        print(end_quote)
        start_requestBody = {
            "symbolName": start,
            "exchange": "NFO",
            "transactionType": "SELL",
            "orderType": "L",
            "quantity": "15",
            "disclosedQuantity": "15",
            "price": start_quote['bestBids'][0]['price'],
            "priceType": "LTP",
            "marketProtection": "1%",
            "orderValidity": "DAY",
            "afterMarketOrderFlag": "NO",
            "productType": "NRML",
            "triggerPrice": "0.00"
        }
        end_requestBody = {
            "symbolName": end,
            "exchange": "NFO",
            "transactionType": "BUY",
            "orderType": "L",
            "quantity": "15",
            "disclosedQuantity": "15",
            "price": end_quote['bestAsks'][0]['price'],
            "priceType": "LTP",
            "marketProtection": "1%",
            "orderValidity": "DAY",
            "afterMarketOrderFlag": "NO",
            "productType": "NRML",
            "triggerPrice": "0.00"
        }
        startout = placeOrder(session_token, start_requestBody)
        print(startout)
        endout = placeOrder(session_token, end_requestBody)
        print(endout)

