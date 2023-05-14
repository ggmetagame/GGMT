import pytest
import logging
from brownie import Wei, reverts
LOGGER = logging.getLogger(__name__)

zero_address = '0x0000000000000000000000000000000000000000'
GGMT_AMOUNT = 1e18 
def helper_issuer_init(accounts,issuer, erc20, ggmv):
    issuer.setGGMV(ggmv, {'from':accounts[0]})
    issuer.setGGMT(erc20, {'from':accounts[0]})
    pools = [(7000, accounts[4]), (2000, accounts[5]), (700, accounts[6]), (200, accounts[7]), (100, accounts[8])]
    tx = issuer. setPools(pools) 

def test_edit_pool(accounts, issuer,erc20, ggmv):
    helper_issuer_init(accounts, issuer,erc20, ggmv)
    logging.info(issuer.getPoolPercents())
    issuer.editPoolByIndex(0, accounts[9], 8000, {'from':accounts[0]})
    assert issuer.getPoolPercents()[0] == (8000, accounts[9])

def test_remove_pool(accounts, issuer):
    logging.info(issuer.getPoolPercents())
    issuer.removePoolByIndex(0, {'from':accounts[0]})
    assert len(issuer.getPoolPercents()) == 4

def test_remove_last_pool(accounts, issuer):
    logging.info(issuer.getPoolPercents())
    issuer.removePoolByIndex(len(issuer.getPoolPercents()) -1, {'from':accounts[0]})
    assert len(issuer.getPoolPercents()) == 3

def test_remove_pools_fail_not_owner(accounts, issuer,erc20, ggmv):
    with reverts('Ownable: caller is not the owner'):
        tx = issuer.removePoolByIndex(0, {'from':accounts[1]})

def test_edit_pool_fail_not_owner(accounts, issuer,erc20, ggmv):
    with reverts('Ownable: caller is not the owner'):
        tx = issuer.editPoolByIndex(0, accounts[9], 8000, {'from':accounts[1]})

def test_edit_pool_fail_not_zero(accounts, issuer,erc20, ggmv):
    with reverts('Not zero address'):
        tx = issuer.editPoolByIndex(0, zero_address, 8000, {'from':accounts[0]})


def test_fail_transferOwnership_not_owner(accounts, issuer,erc20, ggmv):
    with reverts('Ownable: caller is not the owner'):
        tx = issuer.transferOwnership(accounts[9], {'from':accounts[1]})

def test_transferOwnership_ok(accounts, issuer,erc20, ggmv):
    tx = issuer.transferOwnership(accounts[9], {'from':accounts[0]})


def test_fail_set_rate_not_owner(accounts, issuer,erc20, ggmv):
    with reverts('Ownable: caller is not the owner'):
        tx = issuer.setGGMVRate((0,0), {'from':accounts[1]})
 
def test_set_rate_ok(accounts, issuer,erc20, ggmv):
    tx = issuer.setGGMVRate((4,2), {'from':accounts[9]})
    assert issuer.calcTokensForExactGGMT(GGMT_AMOUNT) == GGMT_AMOUNT / issuer.ggmvRate()[0]*issuer.ggmvRate()[1]