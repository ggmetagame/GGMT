from brownie import *
import json

if  web3.eth.chain_id in [4, 5, 97, 1313161555]:
    accounts.load('ttwo');

elif web3.eth.chain_id in [1,56,137, 1313161554]:
    accounts.load('ggmt_deployer')
    
print('Deployer:{}, balance: {}'.format(accounts[0],Wei(accounts[0].balance()).to('ether') ))
print('web3.eth.chain_id={}'.format(web3.eth.chainId))

tx_params = {'from':accounts[0]}
if web3.eth.chainId in  [1,4, 5, 137]:
    tx_params={'from':accounts[0], 'priority_fee': chain.priority_fee}

CHAIN = {   
    0:{'explorer_base':'io', 'premint_address': accounts[0]},
    1:{
        'explorer_base':'etherscan.io', 
        'premint_address': '0x607479d4b8dD98e78b0b80020c6684fd3b83D048',
        'pools':[
            (7000, '0x6858513b3507A5cc172688F460b43401F6a0bC85'), 
            (2000, '0x51850bef51e7Fe134EB6b6eD5B5EC43eef5D3f08'), 
            (700, '0x0db341aDEcA8e05E08E4adAf58a4E0128a62199d'), 
            (200, '0x2c8aDD67fAA83d78EE9a778b883199911A107731'), 
            (100, '0x870F0b051d79264F22f030387a8E7D02A577934d')
        ]
    },
    5:{
        'explorer_base':'goerli.etherscan.io', 
        'premint_address': '0x257F71D96429a550419B760b7809A350Bcc99CA2',
        'pools':[
            (7000, '0x4Da95da9Fd06cc1Ba80F10D8426a83bee7cc4935'), 
            (2000, '0x428Dafb2b991289e0D3e04d160D138C2E859C4Cb'), 
            (700, '0xC254b144B21ea061f0aaEC362bE3905a417483f2'), 
            (200, '0x0960ED5a10f92dEA647A16cfFB50aA5c4c07eeA6'), 
            (100, '0x2398e050150E757481c7e10Dd46E6DcdE186389d')
        ]
    },
    56:{'explorer_base':'bscscan.com', },
    97:{'explorer_base':'testnet.bscscan.com', },
    137:{'explorer_base':'polygonscan.com', },
    80001:{'explorer_base':'mumbai.polygonscan.com', },  
    43114:{'explorer_base':'cchain.explorer.avax.network', },
    43113:{'explorer_base':'cchain.explorer.avax-test.network', },

}.get(web3.eth.chainId, {'explorer_base':'io','premint_address': accounts[0], 
    'pools':[
            (7000, '0x6858513b3507A5cc172688F460b43401F6a0bC85'), 
            (2000, '0x51850bef51e7Fe134EB6b6eD5B5EC43eef5D3f08'), 
            (700, '0x0db341aDEcA8e05E08E4adAf58a4E0128a62199d'), 
            (200, '0x2c8aDD67fAA83d78EE9a778b883199911A107731'), 
            (100, '0x870F0b051d79264F22f030387a8E7D02A577934d')
        ]
})
print(CHAIN)
zero_address = '0x0000000000000000000000000000000000000000'

def main():

    #ggmt = GGMTToken.deploy(CHAIN['premint_address'], tx_params)
    ggmt = GGMTToken.at('0x76aAb5FD2243d99EAc92d4d9EBF23525d3ACe4Ec')
    issuer = GGMVIssuer.deploy(tx_params)
    ggmv = GGMVToken.deploy(issuer.address, tx_params)
    # Print addresses for quick access from console
    print("----------Deployment artifacts-------------------")
    
    print("ggmt= GGMTToken.at('{}')".format(ggmt.address))
    print("issuer = GGMVIssuer.at('{}')".format(issuer.address))
    print("ggmv = GGMVToken.at('{}')".format(ggmv.address))

    print("**GGMT ERC20**")
    print('https://{}/address/{}#code'.format(CHAIN['explorer_base'], ggmt.address))

    print("**issuer**")
    print('https://{}/address/{}#code'.format(CHAIN['explorer_base'], issuer.address))

    print("**GGMV ERC20**")
    print('https://{}/address/{}#code'.format(CHAIN['explorer_base'], ggmv.address))

    if  web3.eth.chainId in [1,4, 5,56, 137, 43114,1313161555,1313161554]:
        #GGMTToken.publish_source(ggmt);
        GGMVIssuer.publish_source(issuer);
        GGMVToken.publish_source(ggmv);
    
    issuer.setGGMV(ggmv, tx_params)
    issuer.setGGMT(ggmt, tx_params)

    tx = issuer.setPools(CHAIN['pools'], {'from':accounts[0]})     
    



### Encoding in python
#from eth_abi import encode_single
#from eth_account.messages import encode_defunct
#encoded_msg = encode_single('(string)',('ETH/USDT',))
#pair_hash = Web3.solidityKeccak(['bytes32'],[encoded])


