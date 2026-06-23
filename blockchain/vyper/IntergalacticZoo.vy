# Vyper Starter — Intergalactic Zoo Registry
# Vyper 0.3.10+  |  EVM smart contract in Python-like syntax

# @version 0.3.10
# @title IntergalacticZooVyper
# @notice Organism registry written in Vyper demonstrating structs,
#         events, access control, and safe arithmetic.

# ---------------------------------------------------------------------------
# Structs
# ---------------------------------------------------------------------------
struct Organism:
    name:         String[64]
    planet:       String[64]
    intelligence: uint8
    owner:        address
    minted_at:    uint256

# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------
event OrganismMinted:
    owner:    indexed(address)
    token_id: indexed(uint256)
    name:     String[64]

event OrganismTransferred:
    sender:   indexed(address)
    receiver: indexed(address)
    token_id: indexed(uint256)

# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------
deployer:       public(address)
next_token_id:  public(uint256)
organisms:      public(HashMap[uint256, Organism])
owned_tokens:   public(HashMap[address, DynArray[uint256, 1024]])
is_minter:      public(HashMap[address, bool])

# ---------------------------------------------------------------------------
# Constructor
# ---------------------------------------------------------------------------
@external
def __init__():
    self.deployer      = msg.sender
    self.is_minter[msg.sender] = True
    self.next_token_id = 0

# ---------------------------------------------------------------------------
# Access helpers
# ---------------------------------------------------------------------------
@internal
def _only_deployer():
    assert msg.sender == self.deployer, "Not deployer"

@internal
def _only_minter():
    assert self.is_minter[msg.sender], "Not minter"

# ---------------------------------------------------------------------------
# Write functions
# ---------------------------------------------------------------------------
@external
def set_minter(minter: address, status: bool):
    self._only_deployer()
    self.is_minter[minter] = status

@external
def mint(
    to:           address,
    name:         String[64],
    planet:       String[64],
    intelligence: uint8,
) -> uint256:
    self._only_minter()
    assert intelligence <= 100, "Intelligence must be 0-100"

    token_id: uint256 = self.next_token_id + 1
    self.next_token_id = token_id

    self.organisms[token_id] = Organism({
        name:         name,
        planet:       planet,
        intelligence: intelligence,
        owner:        to,
        minted_at:    block.timestamp,
    })
    self.owned_tokens[to].append(token_id)
    log OrganismMinted(to, token_id, name)
    return token_id

@external
def transfer(to: address, token_id: uint256):
    assert self.organisms[token_id].minted_at != 0, "Token does not exist"
    assert self.organisms[token_id].owner == msg.sender, "Not owner"
    self.organisms[token_id].owner = to
    self.owned_tokens[to].append(token_id)
    log OrganismTransferred(msg.sender, to, token_id)

# ---------------------------------------------------------------------------
# View functions
# ---------------------------------------------------------------------------
@view
@external
def get_organism(token_id: uint256) -> Organism:
    assert self.organisms[token_id].minted_at != 0, "Token does not exist"
    return self.organisms[token_id]

@view
@external
def tokens_of(owner: address) -> DynArray[uint256, 1024]:
    return self.owned_tokens[owner]
