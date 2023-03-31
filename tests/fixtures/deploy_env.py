import pytest

@pytest.fixture(scope="module")
def erc20(accounts, GGMTToken):
    erc = accounts[0].deploy(GGMTToken, accounts[0])
    yield erc


 



