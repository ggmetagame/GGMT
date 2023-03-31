import pytest
import logging
from brownie import Wei, reverts
LOGGER = logging.getLogger(__name__)


def test_erc20_params(accounts, erc20):
    assert erc20.totalSupply() == erc20.MAX_SUPPLY()
    assert erc20.symbol() == 'GGMT'
    assert erc20.name() == 'Green Grey MetaGame Token'
    assert erc20.decimals() == 18
    assert erc20.MAX_SUPPLY() == 10_000_000_000e18
    assert erc20.balanceOf(accounts[0]) == erc20.totalSupply()

def test_erc20_params(accounts, erc20): 
    with reverts('ERC20: burn amount exceeds balance'):   
        erc20.burn(erc20.MAX_SUPPLY() + 1)
    erc20.burn(erc20.MAX_SUPPLY() - 1)
    assert erc20.balanceOf(accounts[0]) == 1


