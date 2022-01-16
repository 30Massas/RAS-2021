import requests

key = 'a9aacc240a547127a27b72a1'

# Euro - EUR
# Dolar - USD
# Pound - GBP

def requestRate(to_convert,converted):
    url = f'https://v6.exchangerate-api.com/v6/{key}/latest/{to_convert}'
    response = requests.request("GET", url)
    data = response.json()
    return data['conversion_rates'][converted]