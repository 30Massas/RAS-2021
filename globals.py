import coin_api as ca
import math

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

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def round_half_away_from_zero(n, decimals=0):
    rounded_abs = round_half_up(abs(n), decimals)
    return int(math.copysign(rounded_abs, n))

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'