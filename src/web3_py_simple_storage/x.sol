// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 public favNumber = 0;
    // address favAddress  = 0x4175B7Aa527ba2584CC339A485e8486e49E2814C

    struct People {
        uint256 favNum;
        string name;
    }

    // People public person = People({favNum:2, name: "JD Oaktown"});

    People[] public people;
    mapping(string => uint256) public nameToFavNum;

    function store(uint256 _favNum) public {
        favNumber = _favNum;
    }

    function retrieve() public view returns (uint256) {
        return favNumber;
    }

    // function retrieve() public pure { 4 * 5;}
    // memory means data will only be stored during the execution of the function.
    // storage
    function addPerson(string memory _name, uint256 _favNum) public {
        people.push(People(_favNum, _name));
        nameToFavNum[_name] = _favNum;
    }
} //SimpleStorage
