// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title IntergalacticZoo
 * @notice ERC-721-style NFT registry for intergalactic organisms.
 *         Demonstrates: custom errors, events, modifiers, mappings,
 *         structs, enums, access control, and reentrancy guard.
 */

// ---------------------------------------------------------------------------
// Interfaces
// ---------------------------------------------------------------------------
interface IERC165 {
    function supportsInterface(bytes4 interfaceId) external view returns (bool);
}

// ---------------------------------------------------------------------------
// Custom errors (gas-efficient)
// ---------------------------------------------------------------------------
error NotOwner(address caller, uint256 tokenId);
error TokenAlreadyExists(uint256 tokenId);
error TokenDoesNotExist(uint256 tokenId);
error InvalidIntelligence(uint8 value);
error ReentrancyGuardLocked();

// ---------------------------------------------------------------------------
// Main contract
// ---------------------------------------------------------------------------
contract IntergalacticZoo is IERC165 {

    // -----------------------------------------------------------------------
    // Types
    // -----------------------------------------------------------------------
    enum PlanetType { Rocky, GasGiant, IceGiant, Dwarf }

    struct Organism {
        string   name;
        string   planet;
        uint8    intelligence;   // 0–100
        PlanetType planetType;
        address  owner;
        uint256  mintedAt;
    }

    // -----------------------------------------------------------------------
    // State
    // -----------------------------------------------------------------------
    address public immutable deployer;
    uint256 private _nextTokenId;
    bool    private _locked;

    mapping(uint256 => Organism) private _organisms;
    mapping(address => uint256[]) private _ownedTokens;
    mapping(address => bool)       public  authorisedMinters;

    // -----------------------------------------------------------------------
    // Events
    // -----------------------------------------------------------------------
    event OrganismMinted(address indexed owner, uint256 indexed tokenId, string name);
    event OrganismTransferred(address indexed from, address indexed to, uint256 indexed tokenId);
    event MinterAuthorised(address indexed minter, bool status);

    // -----------------------------------------------------------------------
    // Modifiers
    // -----------------------------------------------------------------------
    modifier onlyDeployer() {
        require(msg.sender == deployer, "Not deployer");
        _;
    }

    modifier onlyMinter() {
        require(authorisedMinters[msg.sender] || msg.sender == deployer, "Not minter");
        _;
    }

    modifier tokenExists(uint256 tokenId) {
        if (_organisms[tokenId].mintedAt == 0) revert TokenDoesNotExist(tokenId);
        _;
    }

    modifier nonReentrant() {
        if (_locked) revert ReentrancyGuardLocked();
        _locked = true;
        _;
        _locked = false;
    }

    // -----------------------------------------------------------------------
    // Constructor
    // -----------------------------------------------------------------------
    constructor() {
        deployer = msg.sender;
        authorisedMinters[msg.sender] = true;
    }

    // -----------------------------------------------------------------------
    // Write functions
    // -----------------------------------------------------------------------

    /// @notice Authorise or revoke a minter address.
    function setMinter(address minter, bool status) external onlyDeployer {
        authorisedMinters[minter] = status;
        emit MinterAuthorised(minter, status);
    }

    /// @notice Mint a new organism NFT.
    function mint(
        address to,
        string  calldata name,
        string  calldata planet,
        uint8   intelligence,
        PlanetType planetType
    ) external onlyMinter returns (uint256 tokenId) {
        if (intelligence > 100) revert InvalidIntelligence(intelligence);
        tokenId = ++_nextTokenId;
        _organisms[tokenId] = Organism({
            name:        name,
            planet:      planet,
            intelligence: intelligence,
            planetType:  planetType,
            owner:       to,
            mintedAt:    block.timestamp
        });
        _ownedTokens[to].push(tokenId);
        emit OrganismMinted(to, tokenId, name);
    }

    /// @notice Transfer an organism to another address.
    function transfer(address to, uint256 tokenId)
        external
        tokenExists(tokenId)
        nonReentrant
    {
        Organism storage org = _organisms[tokenId];
        if (org.owner != msg.sender) revert NotOwner(msg.sender, tokenId);
        org.owner = to;
        _ownedTokens[to].push(tokenId);
        emit OrganismTransferred(msg.sender, to, tokenId);
    }

    // -----------------------------------------------------------------------
    // View functions
    // -----------------------------------------------------------------------

    function getOrganism(uint256 tokenId)
        external view
        tokenExists(tokenId)
        returns (Organism memory)
    {
        return _organisms[tokenId];
    }

    function tokensOf(address owner) external view returns (uint256[] memory) {
        return _ownedTokens[owner];
    }

    function totalSupply() external view returns (uint256) {
        return _nextTokenId;
    }

    function supportsInterface(bytes4 interfaceId) external pure override returns (bool) {
        return interfaceId == type(IERC165).interfaceId;
    }
}
