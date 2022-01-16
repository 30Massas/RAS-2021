import coin_api as ca

tipo_moedas = {
    1 : 'EUR',
    2 : 'USD',
    3 : 'GBP',
    4 : 'Cardano'
}

def print_coins():
    for option,coin in tipo_moedas.items():
        print(f'#{option} - {coin}')

def convertCoin(to_convert,converted,amount):
    valor_moeda = ca.requestRate(to_convert,converted)
    return amount*valor_moeda
