// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {Cursed} from "./Cursed.sol";

contract Setup {
    Cursed public cursed;

    constructor() payable {
        cursed = new Cursed();
    }

    function isSolved() public view returns (bool) {
        return cursed._xx__x_x__x();
    }
}
