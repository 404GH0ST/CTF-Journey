// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Test {
    address public test;
    constructor(){
        test = address(10);
    }

    function changeAddress(address _new) public {
        test = _new;
    }

    function changeAddress2(address _new) public payable {
        test = _new;
    }

    receive() external payable { }
}