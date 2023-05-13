// SPDX-License-Identifier: MIT

pragma solidity 0.8.19;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/IERC20Mint.sol";

contract  GGMVIssuer is Ownable {
    using SafeERC20 for IERC20;

    uint256 constant public PERCENT_DENOMINATOR = 100;

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

    function setPoolPercenr(address _pool, uint256 _percent) 
        external 
        onlyOwner 
    {
        require(_pool != address(0), "Not zero address");
        // check  that pool exist in array
        for (uint256 i; i < pools.length; ++ i){
            if (pools[i].pool == _pool) {
                pools[i].percent = _percent;
                return;
            }
        }
        pools.push(PoolPercents(_percent, _pool));

        // check that all pools <=100%
        uint256 sum;
        for (uint256 i; i < pools.length; ++ i){
            sum += pools[i].percent;
        }
        require (sum == 100 * PERCENT_DENOMINATOR, "Pool percent amount must be 100%");
        emit PoolChanged(_pool, _percent);
    }

    function removePoolByIndex(uint256 _poolIndex) 
        external 
        onlyOwner
    {
        if (_poolIndex != pools.length - 1) {
            // just replace deleted item with last item
            pools[_poolIndex] = pools[pools.length - 1];
        } 
        pools.pop();
        emit PoolRemoved(pools[_poolIndex].pool);
    }

    function withdrawERC20(address _erc20) external onlyOwner {
        IERC20(_erc20).transfer(owner(), IERC20(_erc20).balanceOf(address(this)));
    }
    /////////////////////////////////////////////////////////////
    
    function _distributeGGMT(uint256 _GGMTAmount) internal virtual {
        for (uint256 i; i < pools.length; ++ i){
            IERC20(ggmt).safeTransfer(
                pools[i].pool,
                _GGMTAmount * pools[i].percent / PERCENT_DENOMINATOR
            );
            emit PoolsIncome(pools[i].pool, _GGMTAmount * pools[i].percent / PERCENT_DENOMINATOR);
        }

    }

    function _calcTokensForExactGGMT(uint256 _inAmount) internal view virtual returns (uint256){
        return _inAmount / ggmvRate.rate * ggmvRate.denominator;
    }

    function _isBlackListed(address _sender) internal view virtual returns (bool){
        // Pools can`t be sender
        for (uint256 i; i < pools.length; ++ i){
            if (pools[i].pool == msg.sender){
                return true;
            }
        }

        // Not in blacklist
        return blacklist[msg.sender]; 
    }
}