from brownie import network, config, accounts, MockV3Aggregator
# from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ("mainnet-fork", "mainnet-fork-dev", "jdalchemyfork")
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ("development", "jdbrownie")


DECIMALS = 8
STARTING_PRICE = 200000000000

def get_account():
    # print(f"in get_account():\t{network.show_active() = }")
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS+FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    activeNet = network.show_active()
    if len(MockV3Aggregator) < 1:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account() })
        # MockV3Aggregator.deploy(DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()})
    print(f"Mocks deployed: {activeNet = }")



