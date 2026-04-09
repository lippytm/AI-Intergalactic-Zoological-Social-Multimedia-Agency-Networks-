"""
Knowledge Base Module
=====================
The Encyclopedia of Everything Applied — a structured, extensible repository
of knowledge entries spanning education, technology, business, robotics,
blockchain, and wearable tech.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class KnowledgeEntry:
    """A single entry in the encyclopedia."""
    title: str
    category: str
    summary: str
    details: str = ""
    tags: List[str] = field(default_factory=list)
    related_entries: List[str] = field(default_factory=list)

    def display(self, full: bool = False) -> str:
        """Return a formatted entry, optionally including full details."""
        lines = [
            f"[{self.category}] {self.title}",
            f"  {self.summary}",
        ]
        if self.tags:
            lines.append(f"  Tags: {', '.join(self.tags)}")
        if self.related_entries:
            lines.append(f"  See also: {', '.join(self.related_entries)}")
        if full and self.details:
            lines.append("")
            lines.append(self.details)
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Built-in knowledge entries
# ---------------------------------------------------------------------------

_ENTRIES: List[KnowledgeEntry] = [
    KnowledgeEntry(
        title="Blockchain",
        category="Technology",
        summary=(
            "A distributed, append-only ledger secured by cryptographic hashing "
            "and consensus mechanisms."
        ),
        details=(
            "A blockchain consists of an ordered chain of blocks, each containing "
            "a set of transactions and the cryptographic hash of the previous block. "
            "This structure makes retroactive alteration computationally infeasible. "
            "Consensus mechanisms — such as Proof of Work, Proof of Stake, or "
            "Byzantine Fault Tolerant protocols — allow geographically dispersed "
            "nodes to agree on the canonical state of the ledger without trusting "
            "a central authority."
        ),
        tags=["blockchain", "distributed-ledger", "cryptography", "decentralisation"],
        related_entries=["Smart Contract", "Consensus Algorithm", "Cryptographic Hashing"],
    ),
    KnowledgeEntry(
        title="Smart Contract",
        category="Technology",
        summary=(
            "Self-executing code stored on a blockchain that automatically enforces "
            "the terms of an agreement."
        ),
        details=(
            "Smart contracts are programmes deployed to a blockchain network. Once "
            "deployed, their code is immutable and their execution is deterministic "
            "across all validating nodes. They are commonly written in Solidity (for "
            "the Ethereum Virtual Machine) or Rust (for Solana / Near Protocol). "
            "Key use-cases include decentralised finance (DeFi), NFT marketplaces, "
            "supply-chain provenance, and on-chain governance."
        ),
        tags=["smart-contract", "solidity", "ethereum", "automation"],
        related_entries=["Blockchain", "ERC-20", "ERC-721"],
    ),
    KnowledgeEntry(
        title="Wearable Technology",
        category="Technology",
        summary=(
            "Electronic devices worn on or in the body to sense, compute, and "
            "communicate information."
        ),
        details=(
            "Wearable technologies span smartwatches, AR/VR headsets, biometric "
            "patches, exoskeletons, and neural interfaces. They are characterised "
            "by stringent power, weight, and form-factor constraints. Programming "
            "wearables typically involves embedded C/C++, MicroPython, or "
            "TensorFlow Lite for on-device ML inference. In the context of the "
            "Encyclopedia of Everything Applied, wearables serve as embodied "
            "learning tools that bridge physical experience and digital skill-building."
        ),
        tags=["wearable", "embedded", "IoT", "edge-AI", "sensors"],
        related_entries=["Edge AI", "Sensor Fusion", "TinyML"],
    ),
    KnowledgeEntry(
        title="Prompt Engineering",
        category="Artificial Intelligence",
        summary=(
            "The practice of designing and iteratively refining natural-language "
            "instructions to elicit optimal responses from AI language models."
        ),
        details=(
            "Effective prompts specify a role/persona for the model, provide "
            "relevant context, define the output format, include examples "
            "(few-shot prompting), and instruct the model to reason step-by-step "
            "(chain-of-thought prompting). Prompts are iteratively improved by "
            "applying strategies such as narrowing scope, adding constraints, or "
            "requesting alternative perspectives. A good prompt is often more "
            "valuable than a larger model."
        ),
        tags=["AI", "LLM", "prompt-engineering", "chain-of-thought", "few-shot"],
        related_entries=["Large Language Model", "Chain-of-Thought", "Few-Shot Learning"],
    ),
    KnowledgeEntry(
        title="Robotics",
        category="Engineering",
        summary=(
            "The interdisciplinary field combining mechanical engineering, electrical "
            "engineering, and computer science to design and programme autonomous machines."
        ),
        details=(
            "Modern robotics encompasses perception (computer vision, LIDAR, IMUs), "
            "planning (path planning, task planning), and control (PID controllers, "
            "model-predictive control). Robot Operating System (ROS/ROS 2) is the "
            "de-facto framework for building robot software. Machine learning — "
            "particularly reinforcement learning — is increasingly used to train "
            "robots to perform complex tasks without hand-coded rules."
        ),
        tags=["robotics", "ROS", "perception", "control", "reinforcement-learning"],
        related_entries=["ROS 2", "Reinforcement Learning", "Computer Vision"],
    ),
    KnowledgeEntry(
        title="Intergalactic Zoological Society",
        category="Organisation",
        summary=(
            "The governing body responsible for cataloguing, protecting, and "
            "educating all sentient species across the known galaxy."
        ),
        details=(
            "Founded in the 41st century, the Intergalactic Zoological Society (IZS) "
            "maintains the Encyclopedia of Everything Applied as its primary "
            "educational resource. Membership is open to humans, robots, and any "
            "space-faring alien species that passes the Universal Sentience "
            "Assessment. The Society's motto: 'Knowledge without borders, "
            "learning without limits.'"
        ),
        tags=["IZS", "intergalactic", "education", "science-fiction", "lore"],
        related_entries=["Space Alien", "Encyclopedia of Everything Applied"],
    ),
    KnowledgeEntry(
        title="Encyclopedia of Everything Applied",
        category="Education",
        summary=(
            "A living, open-source knowledge base and training platform for all "
            "sentient beings wishing to become better programmers and blockchain "
            "developers."
        ),
        details=(
            "The Encyclopedia of Everything Applied is the flagship product of the "
            "AI Intergalactic Zoological Social Multimedia Agency Networks. It "
            "provides structured curricula, hands-on exercises, wearable-tech "
            "integrations, and AI-powered prompt engineering tools. Its goal is to "
            "make high-quality technical education universally accessible — whether "
            "the learner is a first-year human student, a newly-activated android, "
            "or a centuries-old space alien seeking to upskill in blockchain "
            "development."
        ),
        tags=["encyclopedia", "education", "blockchain", "robotics", "wearable", "AI"],
        related_entries=["Blockchain", "Robotics", "Wearable Technology", "Prompt Engineering"],
    ),
]


class KnowledgeBase:
    """
    The central knowledge repository of the Encyclopedia of Everything Applied.

    Supports full-text search, category filtering, and tag-based discovery.
    """

    def __init__(self) -> None:
        self._entries: Dict[str, KnowledgeEntry] = {
            entry.title: entry for entry in _ENTRIES
        }

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def add_entry(self, entry: KnowledgeEntry) -> None:
        """Add or replace a knowledge entry."""
        self._entries[entry.title] = entry

    def get_entry(self, title: str) -> Optional[KnowledgeEntry]:
        """Return an entry by its exact title."""
        return self._entries.get(title)

    def remove_entry(self, title: str) -> bool:
        """Remove an entry by title. Returns True if it existed."""
        return self._entries.pop(title, None) is not None

    # ------------------------------------------------------------------
    # Search & discovery
    # ------------------------------------------------------------------

    def search(self, query: str) -> List[KnowledgeEntry]:
        """
        Search entries whose title, summary, details, or tags contain the query
        (case-insensitive substring match).
        """
        query_lower = query.lower()
        results = []
        for entry in self._entries.values():
            haystack = " ".join([
                entry.title,
                entry.summary,
                entry.details,
                " ".join(entry.tags),
            ]).lower()
            if query_lower in haystack:
                results.append(entry)
        return results

    def get_by_category(self, category: str) -> List[KnowledgeEntry]:
        """Return all entries in a given category (case-insensitive)."""
        cat_lower = category.lower()
        return [e for e in self._entries.values() if e.category.lower() == cat_lower]

    def get_by_tag(self, tag: str) -> List[KnowledgeEntry]:
        """Return all entries that carry a given tag (case-insensitive)."""
        tag_lower = tag.lower()
        return [e for e in self._entries.values() if tag_lower in [t.lower() for t in e.tags]]

    def list_categories(self) -> List[str]:
        """Return a sorted list of unique categories."""
        return sorted({e.category for e in self._entries.values()})

    def list_all_titles(self) -> List[str]:
        """Return a sorted list of all entry titles."""
        return sorted(self._entries.keys())

    def summarize(self) -> str:
        """Return a human-readable overview of the knowledge base."""
        categories = self.list_categories()
        lines = [
            "=== Encyclopedia of Everything Applied — Knowledge Base ===",
            f"Total entries: {len(self._entries)}",
            f"Categories: {', '.join(categories)}",
            "",
        ]
        for cat in categories:
            entries = self.get_by_category(cat)
            lines.append(f"{cat} ({len(entries)} entries):")
            for e in entries:
                lines.append(f"  • {e.title}")
            lines.append("")
        return "\n".join(lines)
