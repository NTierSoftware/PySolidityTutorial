from brownie import FundMe
from scripts.helpful_scripts import get_account #, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS

fundMe = FundMe[-1]
account = get_account()


def fund():
    # fundMe = FundMe[-1]
    # account = get_account()
    entranceFee = fundMe.getEntranceFee()
    print(f'{entranceFee = }\t ...now funding')
    fundMe.fund({"from": account, "value": entranceFee})

def withdraw():
    fundMe.withdraw({"from": account})

def main():
        fund()
        withdraw()

