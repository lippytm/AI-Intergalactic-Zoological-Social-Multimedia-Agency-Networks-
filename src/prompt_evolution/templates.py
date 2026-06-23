"""Curated prompt templates for the intergalactic zoological theme.

Each template is a seed prompt that can be seeded into a :class:`PromptPopulation`
and then evolved using :class:`PromptEvolver`.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Template library
# ---------------------------------------------------------------------------

PROMPT_TEMPLATES: dict[str, str] = {
    # ── Prompt Engineering ──────────────────────────────────────────────────
    "prompt_meta": (
        "Write a detailed prompt that will guide an AI to generate a highly "
        "structured, factual, and creative response about intergalactic zoology."
    ),
    "prompt_refine": (
        "You are an expert prompt engineer. Given the following draft prompt, "
        "improve it by adding clarity, specificity, and role framing so that an "
        "AI produces a better response: {draft_prompt}"
    ),
    "prompt_evolve": (
        "Act as an evolutionary prompt optimizer. Analyze the weaknesses of the "
        "following prompt and generate three improved variants that score higher on "
        "clarity, specificity, and actionability: {original_prompt}"
    ),
    # ── Intergalactic Zoological Society ────────────────────────────────────
    "zoo_catalog": (
        "You are the chief xenobiologist of the Intergalactic Zoological Society. "
        "Describe five newly discovered alien species, including their habitat, "
        "evolutionary history, and cultural significance to space-faring civilizations."
    ),
    "zoo_ethics": (
        "As an ethics officer at the Intergalactic Zoological Society, outline a "
        "comprehensive policy framework for the ethical treatment of sentient alien "
        "creatures in captivity."
    ),
    # ── Quantum Entanglement & Many Worlds ──────────────────────────────────
    "quantum_narrative": (
        "Imagine you are a quantum-entanglement narrative designer. Create a short "
        "story set across three parallel universes where the protagonist must solve "
        "an ecological crisis using quantum communication."
    ),
    "quantum_teaching": (
        "Explain quantum entanglement to a young space alien who has never encountered "
        "classical physics. Use relatable analogies, diagram descriptions, and "
        "step-by-step reasoning."
    ),
    # ── AI & Robotics Education ─────────────────────────────────────────────
    "ai_teacher": (
        "You are an advanced AI tutor specialising in machine learning for "
        "interspecies learners. Design a 4-week curriculum to teach a robot the "
        "fundamentals of neural networks, including practical exercises."
    ),
    "robotics_wearable": (
        "Act as a wearable-technology engineer. Describe a next-generation exosuit "
        "designed for both humans and space aliens that integrates real-time AI "
        "assistance, blockchain credentialing, and biometric monitoring."
    ),
    # ── Blockchain & Decentralised Systems ──────────────────────────────────
    "blockchain_basics": (
        "Teach a beginner — human or alien — the core concepts of blockchain "
        "technology: distributed ledgers, consensus mechanisms, and smart contracts. "
        "Use concrete examples relevant to interplanetary trade."
    ),
    "blockchain_advanced": (
        "You are a senior blockchain architect. Design a decentralised governance "
        "system for the Intergalactic Zoological Society that enables member "
        "civilisations to vote on conservation policy via tokenised proposals."
    ),
    # ── Time Machines & Systems Management ──────────────────────────────────
    "time_management": (
        "As the chief engineer of the Intergalactic Time Machines Management System, "
        "describe the key protocols required to prevent causal paradoxes when multiple "
        "civilisations share access to a single temporal gateway."
    ),
    # ── Space Aliens Social & Political Party ───────────────────────────────
    "political_manifesto": (
        "You are a political speech writer for the Space Aliens Social Political "
        "Party. Write a manifesto that advocates for universal rights for all "
        "sentient beings across the galaxy, covering education, healthcare, and "
        "environmental protection."
    ),
    # ── Evolutionary Prompt Engineering Meta-Loop ───────────────────────────
    "evolutionary_loop": (
        "You are an evolutionary prompt engineering system. Your task is to: "
        "1) evaluate the quality of a given prompt, "
        "2) identify its weaknesses, "
        "3) generate two mutated variants using different improvement strategies, "
        "4) select the better variant based on clarity and specificity, "
        "5) repeat for three generations. "
        "Begin with the following seed prompt: {seed_prompt}"
    ),
}
