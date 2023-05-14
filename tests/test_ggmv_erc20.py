import pytest
import logging
from brownie import Wei, reverts
LOGGER = logging.getLogger(__name__)

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
GGMT_AMOUNT = 1e18 

def helper_issuer_init(accounts,issuer, erc20, ggmv):
    issuer.setGGMV(ggmv, {'from':accounts[0]})
    issuer.setGGMT(erc20, {'from':accounts[0]})
    pools = [(7000, accounts[4]), (2000, accounts[5]), (700, accounts[6]), (200, accounts[7]), (100, accounts[8])]
    tx = issuer.setPools(pools, {'from':accounts[0]})  

def test_issue_ggmv(accounts, issuer,erc20, ggmv):
    helper_issuer_init(accounts, issuer,erc20, ggmv)
    erc20.approve(issuer, GGMT_AMOUNT * 10, {'from':accounts[0]})
    tx = issuer.getGGMVForExactGGMT(GGMT_AMOUNT * 10, {'from':accounts[0]})
    logging.info(tx.return_value)
    assert len(tx.events['PoolsIncome']) == 5
 ############################################################## 

def test_approve_fail(accounts, ggmv):
    with reverts("ERC20: approve to the zero address"):
        ggmv.approve(ZERO_ADDRESS, 1, {"from": accounts[0]})

def test_transfer_fail(accounts, ggmv):
    with reverts("ERC20: transfer to the zero address"):
        ggmv.transfer(ZERO_ADDRESS, 1, {"from": accounts[0]})

def test_ggmv_transferFrom(accounts, ggmv):
    ggmv.transfer(accounts[1], 1, {"from": accounts[0]})
    with reverts("ERC20: insufficient allowance"):
        ggmv.transferFrom(accounts[1], accounts[2], 1, {"from": accounts[2]})
    ggmv.approve(accounts[0], 1, {"from": accounts[1]})    
    ggmv.transferFrom(accounts[1], accounts[2], 1, {"from": accounts[0]})
    assert ggmv.balanceOf(accounts[1]) == 0
    assert ggmv.balanceOf(accounts[2]) == 1

    #minter
    ggmv.transfer(accounts[1], 1, {"from": accounts[0]})
    ggmv.approve(accounts[2], 1, {"from": accounts[1]})
    ggmv.transferFrom(accounts[1], accounts[2], 1, {"from": accounts[2]})
    assert ggmv.balanceOf(accounts[1]) == 0
    assert ggmv.balanceOf(accounts[2]) == 2

    ggmv.approve(accounts[3], 1, {"from": accounts[1]})
    with reverts("ERC20: transfer amount exceeds balance"):
        ggmv.transferFrom(accounts[1], accounts[3], 1, {"from": accounts[3]})

def test_increaseAllowance(accounts, ggmv):
    before = ggmv.allowance(accounts[1], accounts[3])
    tx = ggmv.increaseAllowance(accounts[3], 1e18, {'from': accounts[1]})
    assert len(tx.events['Approval']) == 1
    assert before == ggmv.allowance(accounts[1], accounts[3]) - 1e18       


def test_decreaseAllowance(accounts, ggmv):
    before = ggmv.allowance(accounts[1], accounts[3])
    tx = ggmv.decreaseAllowance(accounts[3], 1e18, {'from': accounts[1]})
    assert len(tx.events['Approval']) == 1
    assert before == ggmv.allowance(accounts[1], accounts[3]) + 1e18       

def test_decreaseAllowance_fail(accounts, ggmv):
    with reverts("ERC20: decreased allowance below zero"):
        ggmv.decreaseAllowance(accounts[4], 1e18, {'from': accounts[0]})

def test_ggmv_transfer(accounts, ggmv):
    before_balance = ggmv.balanceOf(accounts[0])
    logging.info('acc = {}'.format(ggmv.balanceOf(accounts[0])))
    ggmv.transfer(accounts[0], 1e18, {"from":accounts[0]})
    assert ggmv.balanceOf(accounts[0]) == before_balance
