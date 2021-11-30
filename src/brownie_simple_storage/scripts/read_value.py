from brownie import network, SimpleStorage, accounts, config

def read_contract():
    simpleStorage = SimpleStorage[-1]
    print(f'most recent deployment {simpleStorage = }') #
    print(f'{simpleStorage.retrieve() = }')

def main():
    read_contract()