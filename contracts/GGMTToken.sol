// SPDX-License-Identifier: MIT

//   Green Grey MetaGame Token ERC20

//***************************************************************
// ERC20 part of this contract based on best community practice 
// of https://github.com/OpenZeppelin
// Adapted and amended by IBERGroup, email:maxsizmobile@iber.group; 
// Code released under the MIT License.
////**************************************************************

pragma solidity 0.8.17;

import "./ERC20.sol";

contract GGMTToken is ERC20 {

    uint256 constant public MAX_SUPPLY = 10_000_000_000e18;

    constructor(address initialKeeper)
        ERC20("Green Grey MetaGame Token", "GGMT")
    { 
        //Initial supply mint  - review before PROD
        _mint(initialKeeper, MAX_SUPPLY);
    }
    
    /**
     * @dev Burns `_amount` tokens from the caller's account.
     *
     * Returns a boolean value indicating whether the operation succeeded.
     *
     * Emits a {Transfer} event.
     */
    function burn(uint256 _amount) external returns (bool) {
        _burn(msg.sender, _amount);
        return true;
    }
}

