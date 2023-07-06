## Green Grey MetaGame Token


### Tests
We use Brownie framework for developing and unit test. For run tests
first please [install it](https://eth-brownie.readthedocs.io/en/stable/install.html)

```bash
brownie test
```
Don't forget [ganache](https://www.npmjs.com/package/ganache)

### Deployments Info
Deploy is very simple. You can find workflow in 
[fixtures](./tests/fixtures/deploy_env.py) 


#### Ethereum Mainnet 
Deployed at block 16889176 with addreess 
`0xA5FeD2453da128747d06E937c9493F77941B7B6E` (Keys can be obtain on demand)    
https://etherscan.io/address/0x76aAb5FD2243d99EAc92d4d9EBF23525d3ACe4Ec  
Initial supply keeper is `0x607479d4b8dD98e78b0b80020c6684fd3b83D048`


---
#### Gas Consumption Info
```bash
GGMTToken <Contract>
   ├─ constructor         -  avg:  703600  avg (confirmed):  703600  low:  703600  high:  703600
   ├─ transfer            -  avg:   40444  avg (confirmed):   45068  low:   21951  high:   50948
   ├─ approve             -  avg:   39003  avg (confirmed):   40713  low:   21908  high:   44161
   ├─ increaseAllowance   -  avg:   30243  avg (confirmed):   30243  low:   30243  high:   30243
   ├─ transferFrom        -  avg:   26864  avg (confirmed):   26026  low:   22276  high:   31787
   ├─ decreaseAllowance   -  avg:   26696  avg (confirmed):   30227  low:   23165  high:   30227
   └─ burn                -  avg:   26154  avg (confirmed):   27888  low:   20364  high:   35412
GGMVIssuer <Contract>
   ├─ constructor         -  avg: 1309333  avg (confirmed): 1309333  low: 1309333  high: 1309333
   ├─ setPools            -  avg:  218521  avg (confirmed):  282925  low:   25314  high:  282925
   ├─ getGGMVForExactGGMT -  avg:  122007  avg (confirmed):  233591  low:   22505  high:  282806
   ├─ replacePools        -  avg:   91031  avg (confirmed):  103155  low:   25380  high:  141016
   ├─ setGGMT             -  avg:   43495  avg (confirmed):   43495  low:   43483  high:   43507
   ├─ setGGMV             -  avg:   38728  avg (confirmed):   38728  low:   24328  high:   43528
   ├─ setBlackListStatus  -  avg:   29161  avg (confirmed):   29161  low:   14437  high:   43885
   ├─ setGGMVRate         -  avg:   27520  avg (confirmed):   32492  low:   22548  high:   32492
   ├─ editPoolByIndex     -  avg:   27465  avg (confirmed):   36366  low:   22919  high:   36366
   ├─ transferOwnership   -  avg:   26442  avg (confirmed):   30125  low:   22759  high:   30125
   ├─ withdrawERC20       -  avg:   24462  avg (confirmed):   26168  low:   22757  high:   26168
   └─ removePoolByIndex   -  avg:   24312  avg (confirmed):   25246  low:   21458  high:   29034
GGMVToken <Contract>
   ├─ constructor         -  avg:  756404  avg (confirmed):  756404  low:  756404  high:  756404
   ├─ approve             -  avg:   38594  avg (confirmed):   44142  low:   21953  high:   44146
   ├─ transfer            -  avg:   37818  avg (confirmed):   43108  low:   21951  high:   50888
   ├─ increaseAllowance   -  avg:   30309  avg (confirmed):   30309  low:   30309  high:   30309
   ├─ transferFrom        -  avg:   26848  avg (confirmed):   26015  low:   22265  high:   31765
   ├─ decreaseAllowance   -  avg:   26701  avg (confirmed):   30227  low:   23176  high:   30227
   ├─ mint                -  avg:   22914  avg (confirmed):       0  low:   22914  high:   22914
   └─ burn                -  avg:   21495  avg (confirmed):   20352  low:   20352  high:   22638

```

