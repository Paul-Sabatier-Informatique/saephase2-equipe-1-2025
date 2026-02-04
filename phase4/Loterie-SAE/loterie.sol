// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Loterie {
    address public owner;
    uint public mise;

    struct Participant {
        address payable adresse;
        uint montant;
    }

    Participant[] public participants;
    uint public randNonce = 0;

    constructor(uint _mise) {
        owner = msg.sender;
        mise = _mise;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Accès refusé");
        _;
    }

    function participer() public payable {
        require(msg.sender != owner, "Le propriétaire ne peut pas participer");
        require(msg.value == mise, "Montant incorrect");
        participants.push(Participant(payable(msg.sender), msg.value));
    }

    function getBalance() public view returns (uint) {
        return address(this).balance;
    }

    function getParticipants() public view returns (Participant[] memory) {
        return participants;
    }

    function choisirGagnant() public onlyOwner {
        require(participants.length >= 3, "Il faut au moins 3 participants");
        uint index = random(participants.length);
        address payable gagnant = participants[index].adresse;
        gagnant.transfer(address(this).balance);
        delete participants;
    }

    function random(uint _modulus) private returns (uint) {
        randNonce++;
        return uint(keccak256(abi.encodePacked(block.timestamp, msg.sender, randNonce))) % _modulus;
    }
}
