// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./Chest.sol";

contract Setup {
    Chest public immutable TARGET;
    uint256 public test;

    constructor(uint256[] memory _combinations, uint256 _golden_key) public {
        TARGET = new Chest(_combinations, _golden_key);
    }

    function isSolved() public view returns (bool) {
        return TARGET.locked() == false;
    }
}
