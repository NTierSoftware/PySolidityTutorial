from brownie import SimpleStorage, accounts

def test_deploy():
    # Arrange
    account = accounts[0]
    # account = accounts.load('jdtest')

    #Act
    simplestorage = SimpleStorage.deploy({'from':account})
    starting_value = simplestorage.retrieve()
    expected = 0

    #Assert
    assert starting_value == expected

# brownie test -k test_updating_storage
# brownie test -s --pdb
def test_updating_storage():
    # Arrange
    account = accounts[0]
    simplestorage = SimpleStorage.deploy({'from': account})
    #Act
    expected = 16
    simplestorage.store(expected, {'from':account})

    #Assert
    assert expected == simplestorage.retrieve()
    # assert 5 == 3

