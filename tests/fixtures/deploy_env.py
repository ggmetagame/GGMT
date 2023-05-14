import pytest

@pytest.fixture(scope="module")
def erc20(accounts, GGMTToken):
    erc = accounts[0].deploy(GGMTToken, accounts[0])
    yield erc


@pytest.fixture(scope="module")
def issuer(accounts, GGMVIssuer):
    i = accounts[0].deploy(GGMVIssuer)
    yield i


@pytest.fixture(scope="module")
def ggmv(accounts, GGMVToken, issuer):
    erc = accounts[0].deploy(GGMVToken, issuer)
    yield erc

 



