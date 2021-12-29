tipo_moedas = {
    1 : 'Euro',
    2 : 'Dollar',
    3 : 'Pound',
    4 : 'Cardano'
}

valor_moeda = {
    1 : 1,
    2 : 1.13,
    3 : 0.84,
    4 : 0.8
}

def print_coins():
    for option,coin in tipo_moedas.items():
        print(f'#{option} - {coin}')

def convertEtoD(amount):
    return amount*valor_moeda[2]

def convertEtoP(amount):
    return amount*valor_moeda[3]

def convertEtoC(amount):
    return amount*valor_moeda[4]