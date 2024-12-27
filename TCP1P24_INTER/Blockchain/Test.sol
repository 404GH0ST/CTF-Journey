// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Test {

    function getSlotForArrayElement(uint256 _slot, uint256 _elementIndex) public pure returns (bytes32) {
        bytes32 startingSlotForArrayElements = keccak256(abi.encode(_slot));
        return bytes32(uint256(startingSlotForArrayElements) + _elementIndex);
    }
}

contract DecompiledContract {
    bytes private storedData;

    function getAdjustedLength(uint256 length) private pure returns (uint256) {
        uint256 adjusted = length >> 1;
        if (!(length & 0x1)) {
            adjusted = adjusted & 0x7f;
        }
        require(
            (length & 0x1) - (adjusted < 32) == 0,
            "Panic: Access to incorrectly encoded storage byte array"
        );
        return adjusted;
    }

    fallback() external payable {
        revert();
    }

    function setData(bytes memory data) public payable {
        uint256 adjustedLength = getAdjustedLength(storedData.length);

        if (adjustedLength > 31) {
            // Clear storage if necessary
            uint256 storageSlots = (adjustedLength + 31) >> 5;
            for (uint256 i = 0; i < storageSlots; i++) {
                storedData[i * 32] = 0;
            }
        }

        if (data.length > 31) {
            // Store long data
            for (uint256 i = 0; i < data.length; i += 32) {
                assembly {
                    sstore(
                        add(storedData.slot, div(i, 32)),
                        mload(add(add(data, 32), i))
                    )
                }
            }
        } else {
            // Store short data
            bytes32 shortData;
            assembly {
                shortData := mload(add(data, 32))
            }
            storedData = abi.encodePacked((data.length << 1) | 1, shortData);
        }
    }

    function getData() public view returns (bytes memory) {
        uint256 adjustedLength = getAdjustedLength(storedData.length);
        bytes memory result = new bytes(adjustedLength);

        if (adjustedLength > 0) {
            if (adjustedLength > 31) {
                // Retrieve long data
                for (uint256 i = 0; i < adjustedLength; i += 32) {
                    assembly {
                        mstore(
                            add(add(result, 32), i),
                            sload(add(storedData.slot, div(i, 32)))
                        )
                    }
                }
            } else {
                // Retrieve short data
                assembly {
                    mstore(add(result, 32), sload(storedData.slot))
                }
            }
        }

        return result;
    }
}
