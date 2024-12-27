// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Chest {
    uint256[] private combinations;
    mapping(address => uint256) private golden_key;
    bool public locked = true;
    int256 public treasures = 100_000_000_000;
    uint64 public limit = 10_000;

    constructor(uint256[] memory _combinations, uint256 _golden_key) public {
        combinations = _combinations;
        golden_key[
            address(uint160((combinations[0] >> 86) | combinations[1]))
        ] = _golden_key;
    }

    modifier notSoFastKiddo() {
        require(!locked, "Unlock the chest first");
        _;
    }

    function unlock(uint256 _key) public {
        uint256 _golden_key = golden_key[
            address(uint160((combinations[0] >> 86) | combinations[1]))
        ];
        if (_golden_key == _key) {
            locked = false;
        }
    }

    function loot(int256 _amount) public notSoFastKiddo {
        require(uint64(limit - _amount) <= limit, "Don't be greedy");
        treasures -= _amount;
    }
}
