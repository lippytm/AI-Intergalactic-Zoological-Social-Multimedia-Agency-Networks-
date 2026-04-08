// AssemblyScript — NEAR Protocol smart contract
// Compile & Deploy: near deploy --accountId <account> --wasmFile build/release/zoo.wasm

import {
  context,
  logging,
  PersistentMap,
  PersistentVector,
  storage,
} from "near-sdk-as";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------
@nearBindgen
class Organism {
  constructor(
    public id:           u64,
    public name:         string,
    public planet:       string,
    public intelligence: u8,
    public owner:        string,
    public mintedAt:     u64,
  ) {}
}

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------
const organisms  = new PersistentMap<u64, Organism>("o:");
const ownedByMap = new PersistentMap<string, Array<u64>>("owned:");
const NEXT_ID_KEY = "next_id";

function nextId(): u64 {
  const current = storage.getPrimitive<u64>(NEXT_ID_KEY, 0);
  storage.set<u64>(NEXT_ID_KEY, current + 1);
  return current + 1;
}

// ---------------------------------------------------------------------------
// Contract methods
// ---------------------------------------------------------------------------

/// Mint a new organism.
export function mint(
  to:           string,
  name:         string,
  planet:       string,
  intelligence: u8,
): u64 {
  assert(context.predecessor == context.contractName, "Only contract owner can mint");
  assert(intelligence <= 100, "Intelligence must be 0-100");

  const id = nextId();
  const org = new Organism(id, name, planet, intelligence, to, context.blockTimestamp);
  organisms.set(id, org);

  let owned = ownedByMap.contains(to) ? ownedByMap.getSome(to) : new Array<u64>();
  owned.push(id);
  ownedByMap.set(to, owned);

  logging.log(`Minted organism #${id}: ${name} for ${to}`);
  return id;
}

/// Transfer an organism to a new owner.
export function transfer(tokenId: u64, newOwner: string): void {
  assert(organisms.contains(tokenId), "Token not found");
  const org = organisms.getSome(tokenId);
  assert(org.owner == context.predecessor, "Not owner");
  org.owner = newOwner;
  organisms.set(tokenId, org);

  let owned = ownedByMap.contains(newOwner) ? ownedByMap.getSome(newOwner) : new Array<u64>();
  owned.push(tokenId);
  ownedByMap.set(newOwner, owned);

  logging.log(`Transferred organism #${tokenId} to ${newOwner}`);
}

/// Get organism details.
export function getOrganism(tokenId: u64): Organism | null {
  return organisms.contains(tokenId) ? organisms.getSome(tokenId) : null;
}

/// List token IDs owned by an account.
export function tokensOf(owner: string): Array<u64> {
  return ownedByMap.contains(owner) ? ownedByMap.getSome(owner) : new Array<u64>();
}

/// Total number of organisms minted.
export function totalSupply(): u64 {
  return storage.getPrimitive<u64>(NEXT_ID_KEY, 0);
}
