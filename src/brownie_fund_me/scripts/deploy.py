from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_fund_me():
    account = get_account()
    print(f"{account = }")
    # pass the price feed address to our fundme contract
    #if we're on a persistent network like rinkeby, use the associated address
    # otherwise deploy mocks.
    activeNet = network.show_active()

    if activeNet in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    else:
        price_feed_address = config["networks"][activeNet]["eth_usd_price_feed"]


    # fundMe = FundMe.deploy("0x8A753747A1Fa494EC906cE90E9f37563A8AF630e", {"from": account}, publish_source=True)
    fundMe = FundMe.deploy(price_feed_address,
                           {"from": account},
                           publish_source=config["networks"][activeNet].get("verify"),
                           )
    # print(f"JD! Contract deployed to {fundMe.address}")
    return fundMe


def main(): deploy_fund_me()



