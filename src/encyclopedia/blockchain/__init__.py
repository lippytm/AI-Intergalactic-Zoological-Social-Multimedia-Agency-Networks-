"""
Blockchain Development Curriculum
====================================
Teaching and Training Robots, Space Aliens & People to Become
Better Blockchain Developers!
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class BlockchainPlatform(Enum):
    """Supported blockchain platforms."""
    ETHEREUM = "Ethereum"
    SOLANA = "Solana"
    POLKADOT = "Polkadot"
    COSMOS = "Cosmos"
    HYPERLEDGER = "Hyperledger Fabric"
    GENERIC = "Generic / Platform-agnostic"


@dataclass
class SmartContractExample:
    """A minimal smart-contract code example with explanation."""
    title: str
    platform: BlockchainPlatform
    language: str
    code: str
    explanation: str

    def display(self) -> str:
        """Return a formatted display of the contract example."""
        return (
            f"--- {self.title} ({self.platform.value} / {self.language}) ---\n"
            f"{self.explanation}\n\n"
            f"```{self.language.lower()}\n{self.code}\n```"
        )


@dataclass
class BlockchainLesson:
    """A single blockchain-focused lesson."""
    title: str
    description: str
    key_concepts: List[str] = field(default_factory=list)
    examples: List[SmartContractExample] = field(default_factory=list)
    exercises: List[str] = field(default_factory=list)

    def summarize(self) -> str:
        """Return a brief summary of the lesson."""
        return (
            f"Lesson: {self.title}\n"
            f"  {self.description}\n"
            f"  Key concepts: {', '.join(self.key_concepts)}\n"
            f"  Exercises: {len(self.exercises)}"
        )


# ---------------------------------------------------------------------------
# Built-in lessons
# ---------------------------------------------------------------------------

_LESSONS: List[BlockchainLesson] = [
    BlockchainLesson(
        title="Blockchain Fundamentals",
        description=(
            "Understand what a blockchain is, how consensus works, and why "
            "decentralisation matters."
        ),
        key_concepts=[
            "distributed ledger",
            "consensus mechanism",
            "immutability",
            "cryptographic hashing",
            "blocks and chains",
            "nodes and validators",
        ],
        exercises=[
            "Draw a diagram showing how three nodes reach consensus on a new block.",
            "Compute the SHA-256 hash of the string 'Hello, Intergalactic Blockchain!'",
            "Explain in plain language why altering one block invalidates all later blocks.",
        ],
    ),
    BlockchainLesson(
        title="Wallets, Keys, and Transactions",
        description=(
            "Learn how public/private key pairs secure ownership and how "
            "transactions are constructed and signed."
        ),
        key_concepts=[
            "asymmetric cryptography",
            "public key",
            "private key",
            "digital signature",
            "transaction lifecycle",
            "nonce",
            "gas (Ethereum)",
        ],
        exercises=[
            "Generate a key pair and sign a message using Python's cryptography library.",
            "Build a raw Ethereum transaction object (without broadcasting it).",
            "Explain what happens if a private key is lost.",
        ],
    ),
    BlockchainLesson(
        title="Smart Contracts 101",
        description=(
            "Write, test, and deploy your first smart contract on a test network."
        ),
        key_concepts=[
            "smart contract",
            "Solidity",
            "ABI",
            "bytecode",
            "EVM",
            "deploy and interact",
            "events and logs",
        ],
        examples=[
            SmartContractExample(
                title="Hello Intergalactic — Storage Contract",
                platform=BlockchainPlatform.ETHEREUM,
                language="Solidity",
                code="""\
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title IntergalacticGreeting
/// @notice Stores and retrieves a greeting from anywhere in the galaxy.
contract IntergalacticGreeting {
    string private greeting;

    event GreetingUpdated(address indexed sender, string newGreeting);

    constructor(string memory _greeting) {
        greeting = _greeting;
    }

    function setGreeting(string calldata _greeting) external {
        greeting = _greeting;
        emit GreetingUpdated(msg.sender, _greeting);
    }

    function getGreeting() external view returns (string memory) {
        return greeting;
    }
}""",
                explanation=(
                    "This simple storage contract lets any address on the network "
                    "update a greeting string. It emits an event on every update so "
                    "off-chain listeners can react immediately."
                ),
            )
        ],
        exercises=[
            "Deploy IntergalacticGreeting to a local Hardhat or Foundry network.",
            "Call setGreeting() and verify the GreetingUpdated event was emitted.",
            "Add an owner-only modifier so only the deployer can change the greeting.",
        ],
    ),
    BlockchainLesson(
        title="Tokens and Standards",
        description=(
            "Understand fungible (ERC-20) and non-fungible (ERC-721) token standards."
        ),
        key_concepts=[
            "ERC-20",
            "ERC-721",
            "ERC-1155",
            "token minting and burning",
            "allowances and approvals",
            "NFT metadata",
        ],
        examples=[
            SmartContractExample(
                title="AlienCoin — Minimal ERC-20",
                platform=BlockchainPlatform.ETHEREUM,
                language="Solidity",
                code="""\
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @title AlienCoin
/// @notice The official currency of the Intergalactic Zoological Society.
contract AlienCoin is ERC20 {
    constructor(uint256 initialSupply) ERC20("AlienCoin", "ALIEN") {
        _mint(msg.sender, initialSupply * (10 ** decimals()));
    }
}""",
                explanation=(
                    "AlienCoin extends OpenZeppelin's battle-tested ERC-20 implementation. "
                    "The entire token supply is minted to the deployer on construction."
                ),
            )
        ],
        exercises=[
            "Deploy AlienCoin with an initial supply of 1,000,000 tokens.",
            "Transfer 500 tokens to another address and verify the balances.",
            "Implement an ERC-721 'RobotPassport' NFT with on-chain metadata.",
        ],
    ),
    BlockchainLesson(
        title="Security and Auditing",
        description=(
            "Learn the most common smart-contract vulnerabilities and how to "
            "prevent them."
        ),
        key_concepts=[
            "reentrancy",
            "integer overflow/underflow",
            "access control",
            "front-running",
            "oracle manipulation",
            "static analysis tools",
        ],
        exercises=[
            "Identify the reentrancy bug in the vulnerable Ether wallet example.",
            "Fix the bug using the checks-effects-interactions pattern.",
            "Run Slither on a sample contract and interpret the output.",
        ],
    ),
    BlockchainLesson(
        title="Decentralised Applications (dApps)",
        description=(
            "Connect a front-end to a smart contract using ethers.js and a wallet."
        ),
        key_concepts=[
            "Web3 provider",
            "ethers.js / web3.js",
            "wallet connection",
            "reading contract state",
            "sending transactions",
            "event listening",
        ],
        exercises=[
            "Build a minimal HTML + JS page that connects MetaMask.",
            "Display the current greeting from IntergalacticGreeting contract.",
            "Add a form that lets users update the greeting and shows the tx hash.",
        ],
    ),
]


class BlockchainCurriculum:
    """
    Blockchain development curriculum for the Encyclopedia of Everything Applied.

    Guides all learner types — humans, robots, and space aliens — through the
    complete journey from blockchain fundamentals to production-grade dApps.
    """

    def __init__(self) -> None:
        self._lessons: List[BlockchainLesson] = list(_LESSONS)

    def get_lessons(self) -> List[BlockchainLesson]:
        """Return all blockchain lessons."""
        return list(self._lessons)

    def add_lesson(self, lesson: BlockchainLesson) -> None:
        """Add a custom lesson to the curriculum."""
        self._lessons.append(lesson)

    def get_lesson_by_title(self, title: str) -> Optional[BlockchainLesson]:
        """Return the first lesson whose title matches (case-insensitive)."""
        title_lower = title.lower()
        for lesson in self._lessons:
            if lesson.title.lower() == title_lower:
                return lesson
        return None

    def get_lessons_by_platform(self, platform: BlockchainPlatform) -> List[BlockchainLesson]:
        """Return lessons that include examples for a specific platform."""
        return [
            lesson
            for lesson in self._lessons
            if any(ex.platform == platform for ex in lesson.examples)
        ]

    def summarize(self) -> str:
        """Return a human-readable overview of the blockchain curriculum."""
        lines = ["=== Encyclopedia of Everything Applied — Blockchain Curriculum ===", ""]
        for i, lesson in enumerate(self._lessons, 1):
            lines.append(f"{i}. {lesson.title}")
            lines.append(f"   {lesson.description}")
            lines.append("")
        return "\n".join(lines)
