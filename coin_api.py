import requests

key1 = 'a9aacc240a547127a27b72a1'
key2 = 'f384ce817f75061ebdc062ed7cbde014'

# Euro - EUR
# Dolar - USD
# Pound - GBP
# Cardano - ADA

def requestRate(to_convert,converted):
    if to_convert != 'ADA' and converted != 'ADA':
        url = f'https://v6.exchangerate-api.com/v6/{key1}/latest/{to_convert}'
        response = requests.request("GET", url)
        data = response.json()
        return data['conversion_rates'][converted]
    else:
        if to_convert == 'ADA':
            url  = f'http://api.coinlayer.com/api/live?access_key={key2}&target={converted}&symbols={to_convert}'
        else:
            url  = f'http://api.coinlayer.com/api/live?access_key={key2}&target={to_convert}&symbols={converted}'
        response = requests.request("GET",url)
        data = response.json()
        return data['rates'][converted]