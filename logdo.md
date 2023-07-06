

```python


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
