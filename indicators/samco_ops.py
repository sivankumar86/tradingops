import requests
import json

class samcoAPI:
    def login(self,requestBody):
        headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }

        r = requests.post('https://api.stocknote.com/login'
        , data=json.dumps(requestBody)
        , headers = headers,timeout=60)

        return r.json()

    def getIndexHistory(self,session_token,symbol,fromdate):
        headers = {
            'Accept': 'application/json',
            'x-session-token': session_token
        }

        r = requests.get('https://api.stocknote.com/history/indexCandleData', params={
            'indexName': symbol, 'fromDate': fromdate
        }, headers=headers)
        return r.json()

    def getQuote(self,session_token,symbol):
        headers = {
            'Accept': 'application/json',
            'x-session-token': session_token
        }

        r = requests.get('https://api.stocknote.com/quote/getQuote', params={
            'symbolName': symbol, "exchange": "NFO"
        }, headers=headers)
        return r.json()

    def placeOrder(self,session_token,requestBody):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-session-token': session_token
        }

        r = requests.post('https://api.stocknote.com/order/placeOrder'
                          , data=json.dumps(requestBody)
                          , headers=headers)

        return r.json()