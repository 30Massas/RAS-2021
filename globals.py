import coin_api as ca

tipo_moedas = {
    1 : 'EUR',
    2 : 'USD',
    3 : 'GBP',
    4 : 'ADA'
}

def print_coins():
    for option,coin in tipo_moedas.items():
        print(f'#{option} - {coin}')

def convertCoin(to_convert,converted,amount):
    valor_moeda = ca.requestRate(to_convert,converted)
    if to_convert == 'ADA' or converted == 'ADA':
        if to_convert == 'ADA':
            return valor_moeda*amount
        elif converted == 'ADA':
            return amount/valor_moeda
    return amount*valor_moeda
