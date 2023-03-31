

```python


```


### 2023-01-20 Deploy in Testnet
https://testnet.bscscan.com/address/0xe80028240C5d648ACd72448fef378e1D0c838087

```python
badadao= BadaDAO.at('0xe80028240C5d648ACd72448fef378e1D0c838087')
```

### 2023-01-20 Deploy in Production
https://bscscan.com/address/0x94C0fD56c63F323A14b398279327397Db8195eb6

```python
INITIAL_TOKEN_KEEPER = '0xCa894651c02041e29DedA4360545e68018746046'

BadaDAO.deploy(INITIAL_TOKEN_KEEPER, {'from':accounts[0]}, publish_source = True)
badadao= BadaDAO.at('0x94C0fD56c63F323A14b398279327397Db8195eb6')
```
deployer 0xE89805cc1d8D2011478f02Cef20f5E03dd412E25
?quathNofBoor9