import pytest
import logging
from brownie import Wei, reverts
LOGGER = logging.getLogger(__name__)

GGMT_AMOUNT = 1e18 
def helper_issuer_init(accounts,issuer, erc20, ggmv):
    issuer.setGGMV(ggmv, {'from':accounts[0]})
    issuer.setGGMT(erc20, {'from':accounts[0]})
    pools = [(7000, accounts[4]), (2000, accounts[5]), (700, accounts[6]), (200, accounts[7]), (100, accounts[8])]
    with reverts('Ownable: caller is not the owner'):
        tx = issuer.setPools(pools, {'from':accounts[1]}) 
    tx = issuer.setPools(pools, {'from':accounts[0]})     

def test_issue_ggmv_fail_not_init(accounts, issuer,erc20, ggmv):
    with reverts('Tokens not Define'):
        tx = issuer.getGGMVForExactGGMT(0, {'from':accounts[0]})
    issuer.setGGMV(ggmv, {'from':accounts[0]})
    with reverts('Tokens not Define'):
        tx = issuer.getGGMVForExactGGMT(0, {'from':accounts[0]})

def test_getter_params(accounts, issuer,erc20, ggmv):
    helper_issuer_init(accounts, issuer,erc20, ggmv)
    logging.info(issuer.getPoolPercents())
    rate = issuer.ggmvRate()
    assert  rate == (1,1)
    assert len(issuer.getPoolPercents()) == 5
    assert issuer.calcTokensForExactGGMT(GGMT_AMOUNT) == GGMT_AMOUNT / rate[0]*rate[1]

def test_issue_ggmv(accounts, issuer,erc20, ggmv):
    ggmv_before = ggmv.balanceOf(accounts[0])
    erc20.approve(issuer, GGMT_AMOUNT, {'from':accounts[0]})
    logging.info(erc20.balanceOf(accounts[0]))
    tx = issuer.getGGMVForExactGGMT(GGMT_AMOUNT, {'from':accounts[0]})
    logging.info(tx.return_value)
    assert ggmv.balanceOf(accounts[0]) == ggmv_before + GGMT_AMOUNT
    assert len(tx.events['PoolsIncome']) == 5
    total_income = 0
    for e in tx.events['PoolsIncome']:
        total_income += e['amount']
    assert total_income == GGMT_AMOUNT    

def test_issue_ggmv_2(accounts, issuer,erc20, ggmv):
    erc20.transfer(accounts[1], GGMT_AMOUNT *2, {'from':accounts[0]})
    ggmv_before = ggmv.balanceOf(accounts[1])
    erc20.approve(issuer, GGMT_AMOUNT/2, {'from':accounts[1]})
    tx = issuer.getGGMVForExactGGMT(GGMT_AMOUNT/2, {'from':accounts[1]})
    assert ggmv.balanceOf(accounts[1]) == ggmv_before + GGMT_AMOUNT/2
    assert len(tx.events['PoolsIncome']) == 5
    total_income = 0
    for e in tx.events['PoolsIncome']:
        total_income += e['amount']
    assert total_income == GGMT_AMOUNT/2  
    assert erc20.balanceOf(issuer) == 0

def test_issue_ggmv_fail_blacklisted(accounts, issuer,erc20, ggmv):
    issuer.setBlackListStatus(accounts[1], True, {'from':accounts[0]})
    erc20.approve(issuer, GGMT_AMOUNT/2, {'from':accounts[1]})
    with reverts('Pool or Blacklisted sender'):
        tx = issuer.getGGMVForExactGGMT(GGMT_AMOUNT/2, {'from':accounts[1]})
    erc20.approve(issuer, erc20.balanceOf(accounts[4]), {'from':accounts[4]})
    with reverts('Pool or Blacklisted sender'):
        tx = issuer.getGGMVForExactGGMT(erc20.balanceOf(accounts[4]), {'from':accounts[4]})

def test_issue_ggmv_fail_zero(accounts, issuer,erc20, ggmv):
    issuer.setBlackListStatus(accounts[1], False, {'from':accounts[0]})
    erc20.approve(issuer, GGMT_AMOUNT/2, {'from':accounts[1]})
    with reverts('Cant mint zero'):
        tx = issuer.getGGMVForExactGGMT(0, {'from':accounts[1]})

def test_issue_ggmv_3(accounts, issuer,erc20, ggmv):
    ggmv_before = ggmv.balanceOf(accounts[1])
    erc20.approve(issuer, 1, {'from':accounts[1]})
    tx = issuer.getGGMVForExactGGMT(1, {'from':accounts[1]})
    assert ggmv.balanceOf(accounts[1]) == ggmv_before + 1
    assert len(tx.events['PoolsIncome']) == 5
    total_income = 0
    for e in tx.events['PoolsIncome']:
        total_income += e['amount']
    assert total_income == 0  
    assert erc20.balanceOf(issuer) == 1

def test_withdraw_erc20_fail_not_owner(accounts, issuer,erc20, ggmv):
    with reverts('Ownable: caller is not the owner'):
        tx = issuer.withdrawERC20(erc20, {'from':accounts[1]})

def test_withdraw_erc20_ok(accounts, issuer,erc20, ggmv):
    erc20_before = erc20.balanceOf(accounts[0])
    tx = issuer.withdrawERC20(erc20, {'from':accounts[0]})
    assert tx.events['Transfer']['value'] == 1
    assert erc20.balanceOf(issuer) == 0
    assert erc20.balanceOf(accounts[0]) == erc20_before + 1

def test_replace_pools_fail_not_owner(accounts, issuer,erc20, ggmv):
    pools = [(7000, accounts[4]), (2000, accounts[5]), (700, accounts[6]), (200, accounts[7]), (100, accounts[8])]
    with reverts('Ownable: caller is not the owner'):
        tx = issuer.replacePools(pools, {'from':accounts[1]})

def test_replace_pools_ok(accounts, issuer,erc20, ggmv):
    pools = [(6000, accounts[4]), (3000, accounts[5]), (700, accounts[6]), (200, accounts[7]), (100, accounts[8])]
    tx = issuer.replacePools(pools, {'from':accounts[0]})        
    assert issuer.getPoolPercents() == pools

def test_replace_pools_fail_zero_address(accounts, issuer,erc20, ggmv):
    zero_address = '0x0000000000000000000000000000000000000000'
    pools = [(7000, zero_address), (2000, accounts[5]), (700, accounts[6]), (200, accounts[7]), (100, accounts[8])]
    with reverts('Not zero address'):
        tx = issuer.replacePools(pools, {'from':accounts[0]})

def test_replace_pools_fail_not_100(accounts, issuer,erc20, ggmv):
    pools = [(0, accounts[4]), (2000, accounts[5]), (700, accounts[6]), (200, accounts[7]), (100, accounts[8])]
    with reverts('Pool percent amount must be 100%'):
        tx = issuer.replacePools(pools, {'from':accounts[0]})

def test_burn_ggmt(accounts, erc20):
    tx = erc20.burn(erc20.balanceOf(accounts[1]), {'from':accounts[1]})
    assert erc20.balanceOf(accounts[1]) == 0
    assert tx.events['Transfer']['value'] > 0

def test_burn_ggmv(accounts, ggmv):
    tx = ggmv.burn(ggmv.balanceOf(accounts[1]), {'from':accounts[1]})
    assert ggmv.balanceOf(accounts[1]) == 0    
    assert tx.events['Transfer']['value'] > 0
   
def test_burn_ggmv_fail(accounts, ggmv):
    with reverts('ERC20: burn amount exceeds balance'):
        ggmv.burn(ggmv.balanceOf(accounts[0])*2, {'from':accounts[0]})
        
def test_mint_ggmv_fail(accounts, ggmv):
    with reverts('Only distibutor contract'):
        ggmv.mint(accounts[0], GGMT_AMOUNT, {'from':accounts[0]})
