# Blockchain Languages Library

Smart-contract and chain-native language examples implementing a consistent
**Intergalactic Zoo Organism Registry** across every major blockchain VM/runtime.

| Language / Platform | File | Toolchain |
|---|---|---|
| **Solidity** (EVM — Ethereum, Polygon, BNB …) | [`solidity/IntergalacticZoo.sol`](./solidity/IntergalacticZoo.sol) | Hardhat / Foundry |
| **Vyper** (EVM — Python-like) | [`vyper/IntergalacticZoo.vy`](./vyper/IntergalacticZoo.vy) | Vyper compiler / Foundry |
| **Rust / Anchor** (Solana) | [`rust-anchor/lib.rs`](./rust-anchor/lib.rs) | Anchor 0.29 |
| **Move** (Aptos / Sui) | [`move/zoo.move`](./move/zoo.move) | Aptos CLI / Sui CLI |
| **Cadence** (Flow) | [`cadence/IntergalacticZoo.cdc`](./cadence/IntergalacticZoo.cdc) | Flow CLI |
| **ink!** (Polkadot / Substrate) | [`ink/lib.rs`](./ink/lib.rs) | cargo-contract 4.x |
| **Cairo** (StarkNet) | [`cairo/zoo.cairo`](./cairo/zoo.cairo) | Scarb |
| **Clarity** (Stacks) | [`clarity/zoo.clar`](./clarity/zoo.clar) | Clarinet |
| **Tact** (TON) | [`tact/zoo.tact`](./tact/zoo.tact) | Blueprint |
| **AssemblyScript** (NEAR) | [`assemblyscript-near/zoo.ts`](./assemblyscript-near/zoo.ts) | near-sdk-as |

## Common Functionality

Every contract implements the same conceptual interface:

```
mint(to, name, planet, intelligence) → tokenId
transfer(tokenId, newOwner)
getOrganism(tokenId) → Organism
totalSupply() → uint
```

## Key Concepts Demonstrated

- **Custom errors** (gas-efficient on EVM)
- **Events / logging** for off-chain indexers
- **Access control** (owner / minter whitelist)
- **Reentrancy protection** (Solidity)
- **Storage patterns** specific to each VM
- **Safe arithmetic** (overflow checks)
