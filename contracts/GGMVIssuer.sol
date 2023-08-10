// SPDX-License-Identifier: MIT

pragma solidity 0.8.19;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/IERC20Mint.sol";

contract  GGMVIssuer is Ownable {
    using SafeERC20 for IERC20;

    uint256 constant public PERCENT_DENOMINATOR = 10000;

    struct Rate {
        uint256 rate;
        uint256 denominator;
    }

    struct PoolPercents{
        uint256 percent; // Multiplied 100 (PERCENT_DENOMINATOR), e.c. 1% - 100, 12% - 1200 
        address pool;
    }

    Rate public ggmvRate; // Price of GGMV expressed in GGMT 
    IERC20Mint public ggmv;
    IERC20 public ggmt;

    PoolPercents[] public pools; 

    mapping(address => bool) public blacklist;

    event PoolsIncome(address indexed pool, uint256 amount);
    event PoolChanged(address indexed pool, uint256 percent);
    event PoolRemoved(address indexed pool);

    constructor(){
        ggmvRate = Rate(1,1);
    }

    function getGGMVForExactGGMT(uint256 _GGMTAmount) external returns (uint256 GGMVAmount){
        // 1. Some checks
        // TODO not to small
        require(
            address(ggmv) != address(0) && address(ggmt) != address(0)
            , 'Tokens not Define'
        );

        require(!_isBlackListed(msg.sender), "Pool or Blacklisted sender");

        // 2. Receive payment
        IERC20(ggmt).safeTransferFrom(msg.sender, address(this), _GGMTAmount);

        // 3. Calc mintable tokens
        GGMVAmount = _calcTokensForExactGGMT(_GGMTAmount);
        require(GGMVAmount > 0, 'Cant mint zero');
        
               
        // 4. Mint ggmv token
        ggmv.mint(msg.sender, GGMVAmount);

        // 5. Distrib received GGMT
        _distributeGGMT(_GGMTAmount);
         
    }

    function getPoolPercents() external view returns(PoolPercents[] memory){
        return pools;
    }

    function calcTokensForExactGGMT(uint256 _GGMTAmount) external view returns(uint256){
        return _calcTokensForExactGGMT(_GGMTAmount);
    }
    ///////////////////////////////////////////////////////////
    ///////    Admin Functions        /////////////////////////
    ///////////////////////////////////////////////////////////
    function setGGMV(address _ggmv) 
        external 
        onlyOwner 
    {
        ggmv = IERC20Mint(_ggmv);
    }

    function setGGMT(address _ggmt) 
        external 
        onlyOwner 
    {
        ggmt = IERC20(_ggmt);
    }

    function setGGMVRate(Rate calldata _rate) 
        external 
        onlyOwner 
    {
        ggmvRate = _rate;
    }

    function setPools(PoolPercents[] calldata _pools) 
        public 
        onlyOwner 
    {
        
        for (uint256 i; i < _pools.length; ++ i){
            require(_pools[i].pool != address(0), "Not zero address");
            pools.push(_pools[i]);
            emit PoolChanged(_pools[i].pool, _pools[i].percent);
        }

        // check that all pools <=100%
        uint256 sum;
        for (uint256 i; i < pools.length; ++ i){
            sum += pools[i].percent;
            
        }
        require (sum == PERCENT_DENOMINATOR, "Pool percent amount must be 100%");
        
    }

    function replacePools(PoolPercents[] calldata _pools) 
        external 
        onlyOwner 
    {
        // remove old pools
        for (uint256 i = pools.length; i > 0; -- i){
            pools.pop();
        }
        setPools(_pools);

    }

    function editPoolByIndex(uint256 _poolIndex, address _pool, uint256 _percent) 
        external 
        onlyOwner
    {
        require(_pool != address(0), "Not zero address");
        pools[_poolIndex] = PoolPercents(_percent, _pool);
        emit PoolChanged(_pool, _percent);

    }

    function removePoolByIndex(uint256 _poolIndex) 
        external 
        onlyOwner
    {
        address _toRemove = pools[_poolIndex].pool;
        if (_poolIndex != pools.length - 1) {
            // just replace deleted item with last item
            pools[_poolIndex] = pools[pools.length - 1];
        } 
        pools.pop();
        emit PoolRemoved(_toRemove);
    }

    function setBlackListStatus(address _addr, bool _isBlack) 
        external 
        onlyOwner 
    {
        blacklist[_addr] = _isBlack;
    }

    function withdrawERC20(address _erc20) external onlyOwner {
        IERC20(_erc20).transfer(owner(), IERC20(_erc20).balanceOf(address(this)));
    }
    /////////////////////////////////////////////////////////////
    
    function _distributeGGMT(uint256 _GGMTAmount) internal virtual {
        for (uint256 i; i < pools.length; ++ i){
            PoolPercents memory pl = pools[i];
            uint256 amount = pl.percent * _GGMTAmount  / PERCENT_DENOMINATOR;
            IERC20(ggmt).safeTransfer(
                pl.pool,
                amount
            );
            emit PoolsIncome(pl.pool, amount);
        }

    }

    function _calcTokensForExactGGMT(uint256 _inAmount) internal view virtual returns (uint256){
        return _inAmount * ggmvRate.denominator / ggmvRate.rate ;
    }

    function _isBlackListed(address _sender) internal view virtual returns (bool){
        // Pools can`t be sender
        // for (uint256 i; i < pools.length; ++ i){
        //     if (pools[i].pool == msg.sender){
        //         return true;
        //     }
        // }

        // Not in blacklist
        return blacklist[msg.sender]; 
    }
}