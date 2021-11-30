# brownie accounts new jdtest
# brownie accounts list
# brownie accounts jdtest
# brownie run deploy.py

from brownie import accounts, config, SimpleStorage, network

def main():
    deploy_simple_storage()


def deploy_simple_storage():
    account = get_account()
    simplestorage = SimpleStorage.deploy({'from':account})
    print(f'{simplestorage.retrieve() = }\n\n'  )
    # transaction = simplestorage.store(16, {'from':account})

    transaction = simplestorage.store(16)
    transaction.wait(1)
    # storedValue = simplestorage.retrieve()
    print(f'{simplestorage.retrieve() = }'  )



def get_account():
    match network.show_active():
        case "development": return accounts[0]

    return accounts.add(config["wallets"]["from_key"])

    # if (network.show_active() == "development"):
    #     return accounts[0]
    #
    # return accounts.add(config["wallets"]["from_key"])
