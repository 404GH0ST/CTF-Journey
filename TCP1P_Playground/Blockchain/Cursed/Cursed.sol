// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Cursed {
    bool public _xx__x_x__x = false; 

    function ___x_x__x_() public view returns (uint256) {
        return (uint128(uint64(uint32(uint256(keccak256(abi.encodePacked(uint256(blockhash(block.number - 1 ^ block.timestamp)))))))));
    }  

    function x__x_xx__(uint256 _x__x) public {
        require(_x__x == ___x_x__x_());
        _xx__x_x__x = true;
    }
}