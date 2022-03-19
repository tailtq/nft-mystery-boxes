// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract TaiWorld is ERC721URIStorage, VRFConsumerBase, Ownable {
    // randomness retriever
    bytes32 public keyHash;
    uint256 public fee;
    // storing data when requesting randomness
    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToName;
    Character[] public characters;
    // configuration
    uint256 public maxTokens;
    uint256 public usdCreateCharacterFee;
    string baseURI;

    AggregatorV3Interface internal ethUsdPriceFeed;

    struct Character {
        string name;
        uint256 strength;
        uint256 dexterity;
        uint256 constitution;
        uint256 intelligence;
        uint256 wisdom;
        uint256 charisma;
        uint256 experience;
    }

    event RequestedCharacter(bytes32 requestId, address sender);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee,
        address _priceFeedAddress,
        uint256 _maxTokens,
        uint256 _usdCreateCharacterFee,
        string memory _baseURI
    )
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("TaiWorld", "TW")
        Ownable()
    {
        fee = _fee;
        keyHash = _keyHash;
        maxTokens = _maxTokens;
        usdCreateCharacterFee = _usdCreateCharacterFee * 10**18;
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        baseURI = _baseURI;
    }

    function createCharacter(string memory name) public payable {
        require(
            characters.length < maxTokens,
            "The number of characters required is fulfilled"
        );
        require(
            msg.value >= getCreateCharacterFee(),
            "The fee to create a new character is not enough"
        );
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        requestIdToName[requestId] = name;
        emit RequestedCharacter(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        uint256 newId = characters.length;
        uint256 strength = (randomNumber % 100);
        uint256 dexterity = ((randomNumber % 10000) / 100);
        uint256 constitution = ((randomNumber % 1000000) / 10000);
        uint256 intelligence = ((randomNumber % 100000000) / 1000000);
        uint256 wisdom = ((randomNumber % 10000000000) / 100000000);
        uint256 charisma = ((randomNumber % 1000000000000) / 10000000000);
        uint256 experience = 0;

        characters.push(
            Character(
                requestIdToName[requestId],
                strength,
                dexterity,
                constitution,
                intelligence,
                wisdom,
                charisma,
                experience
            )
        );
        _safeMint(requestIdToSender[requestId], newId);
        // emit event
    }

    function getNumberOfCharacters() public view returns (uint256) {
        return characters.length;
    }

    function getCharacter(uint256 tokenId)
        public
        view
        returns (
            uint256,
            uint256,
            uint256,
            uint256,
            uint256,
            uint256,
            uint256
        )
    {
        return (
            characters[tokenId].strength,
            characters[tokenId].dexterity,
            characters[tokenId].constitution,
            characters[tokenId].intelligence,
            characters[tokenId].wisdom,
            characters[tokenId].charisma,
            characters[tokenId].experience
        );
    }

    function getLevel(uint256 tokenId) public view returns (uint256) {
        return sqrt(characters[tokenId].experience);
    }

    function sqrt(uint256 x) internal view returns (uint256 y) {
        uint256 z = (x + 1) / 2;
        y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
    }

    function setCreateCharacterFee(uint256 _usdCreateCharacterFee)
        public
        onlyOwner
    {
        usdCreateCharacterFee = _usdCreateCharacterFee;
    }

    function getCreateCharacterFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10;
        uint256 costToCreate = (usdCreateCharacterFee * 10**18) / adjustedPrice;
        return costToCreate;
    }

    function setCID(uint256 tokenId, string memory cid) public onlyOwner {
        require(_exists(tokenId), "Token doesn't exist");
        require(
            bytes(super.tokenURI(tokenId)).length ==
                abi.encodePacked(baseURI, Strings.toString(tokenId)).length,
            "URI already exists. It cannot be modified"
        );
        _setTokenURI(tokenId, cid);
    }

    function setMaxTokens(uint256 _maxTokens) public onlyOwner {
        maxTokens = _maxTokens;
    }

    function setBaseURI(string memory _baseURI) public onlyOwner {
        baseURI = _baseURI;
    }

    function _baseURI() internal view override returns (string memory) {
        return baseURI;
    }

    function withdraw() public onlyOwner {
        uint256 balance = address(this).balance;
        payable(msg.sender).transfer(balance);
    }
}
