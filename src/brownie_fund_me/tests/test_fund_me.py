from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest

def test_can_fund_and_withdraw():
    account = get_account()
    print(f'test_can_fund_and_withdraw: {account = }')
    fundMe = deploy_fund_me()
    entranceFee = fundMe.getEntranceFee() + 100
    tx = fundMe.fund({"from": account, "value": entranceFee})
    tx.wait(1)
    assert fundMe.addressToAmountFunded(account.address) == entranceFee

    tx2 = fundMe.withdraw({"from": account})
    tx2.wait(1)
    assert fundMe.addressToAmountFunded(account.address) == 0



def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip(f"test_only_owner_can_withdraw() is only for local testing: {network.show_active() = }")

    fundMe = deploy_fund_me()
    bad_actor = accounts.add()
    print(f'{bad_actor = }')
    with pytest.raises((exceptions.VirtualMachineError)):
        fundMe.withdraw({"from": bad_actor})

