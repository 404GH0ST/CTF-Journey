// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Attacker {  
    address public owner;
    Victim public vic;

    event check(address);

    constructor(address _vic, address _owner){
        owner = _owner;
        vic = Victim(_vic);
    }

    function getOwner() public view returns (address){
        return vic.owner();
    }

    function getWho() public view returns (address){
        return vic.who();
    }

    function getHm() public  view returns (uint256){
        return vic.hmm();
    }
    
    fallback() external payable {
        emit check(msg.sender); 
        address(vic).delegatecall(msg.data);
    }
}

contract Victim {
    address public owner;
    address public who;
    uint256 public hmm = 10;

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    constructor(){
        owner = msg.sender;
        who = address(0x1337);
    }

    function changeWho(address _new) public onlyOwner{
        who = _new;
    }

    function changeHm(uint256 _new) public onlyOwner {
        hmm = _new;
    }
}

contract ThirdParty {
    Victim public test;

    constructor(){
        test = new Victim();
    }

    function attack(address _to) public {
        (bool transfered, ) = payable(_to).call(abi.encodePacked(abi.encodeWithSignature("changeHm(uint256)", 100)));
        require(transfered, "Failed to Transfer Credit!");
    }
}