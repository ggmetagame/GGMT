### 2023-07-06 Deploy in Ethereum Mainnet
----------Deployment artifacts-------------------

**GGMT ERC20**
https://etherscan.io/address/0x76aAb5FD2243d99EAc92d4d9EBF23525d3ACe4Ec#code
**issuer**
https://etherscan.io/address/0xf61CD8907d95E9BADDDe4CE64816A63B4f1cB12D#code
**GGMV ERC20**
https://etherscan.io/address/0xaB920C4B41F6071f0028F344c397420E374089e7#code

```python

ggmt= GGMTToken.at('0x76aAb5FD2243d99EAc92d4d9EBF23525d3ACe4Ec')
issuer = GGMVIssuer.at('0xf61CD8907d95E9BADDDe4CE64816A63B4f1cB12D')
ggmv = GGMVToken.at('0xaB920C4B41F6071f0028F344c397420E374089e7')



```


### 2023-05-20 Deploy in Testnet
----------Deployment artifacts-------------------

**GGMT ERC20**
https://goerli.etherscan.io/address/0xC47E36B9b91305359f9610d91F54B67b8CfAC12B#code
**issuer**
https://goerli.etherscan.io/address/0x00eCF037DA7616772cc10f1a98C0819350900DBF#code
**GGMV ERC20**
https://goerli.etherscan.io/address/0x7Fe48EE4FBAE0aAf9540688951208D0D5609b860#code

```python
tx_params={'from':accounts[0], 'priority_fee': chain.priority_fee}

ggmt= GGMTToken.at('0xC47E36B9b91305359f9610d91F54B67b8CfAC12B')
issuer = GGMVIssuer.at('0x00eCF037DA7616772cc10f1a98C0819350900DBF')
ggmv = GGMVToken.at('0x7Fe48EE4FBAE0aAf9540688951208D0D5609b860')


```
