"""
Prompt Engineering Module
==========================
Prompts building better Prompts.

Provides tools to craft, refine, and iteratively improve AI prompts for
educational, business, and technical purposes across all learner types.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class PromptCategory(Enum):
    """Category of a prompt's intended use."""
    EDUCATIONAL = "educational"
    TECHNICAL = "technical"
    CREATIVE = "creative"
    BUSINESS = "business"
    BLOCKCHAIN = "blockchain"
    ROBOTICS = "robotics"
    WEARABLE_TECH = "wearable_tech"
    GENERAL = "general"


@dataclass
class Prompt:
    """A single AI prompt with metadata for iterative improvement."""
    text: str
    category: PromptCategory
    version: int = 1
    tags: List[str] = field(default_factory=list)
    parent_prompt: Optional["Prompt"] = field(default=None, repr=False)
    improvement_notes: str = ""

    def __str__(self) -> str:
        return self.text

    def summarize(self) -> str:
        """Return a human-readable summary of the prompt."""
        return (
            f"[v{self.version}] ({self.category.value}) {self.text[:80]}"
            + ("..." if len(self.text) > 80 else "")
        )


# ---------------------------------------------------------------------------
# Built-in prompt templates
# ---------------------------------------------------------------------------

_TEMPLATES: Dict[PromptCategory, str] = {
    PromptCategory.EDUCATIONAL: (
        "You are an expert educator teaching {topic} to a {learner_type} at the "
        "{skill_level} level. Explain {concept} using simple language, relevant "
        "examples, and step-by-step exercises. Encourage questions and provide "
        "positive reinforcement."
    ),
    PromptCategory.TECHNICAL: (
        "You are a senior software engineer with deep expertise in {topic}. "
        "Provide a detailed, technically accurate explanation of {concept}, "
        "including code examples in {language}, best practices, common pitfalls, "
        "and performance considerations."
    ),
    PromptCategory.BLOCKCHAIN: (
        "You are a blockchain architect and smart-contract developer. Explain "
        "{concept} in the context of {platform} blockchain development. Include "
        "working code examples, security considerations, gas optimization tips, "
        "and references to relevant EIPs or standards."
    ),
    PromptCategory.ROBOTICS: (
        "You are a robotics engineer specializing in {robot_type} systems. "
        "Describe how to implement {task} using {framework}. Include sensor "
        "integration, actuator control, safety constraints, and real-time "
        "processing requirements."
    ),
    PromptCategory.WEARABLE_TECH: (
        "You are an embedded-systems engineer specializing in wearable devices. "
        "Explain how to implement {feature} on a {device_type} wearable. Address "
        "power consumption, memory constraints, sensor fusion, and user-experience "
        "considerations."
    ),
    PromptCategory.BUSINESS: (
        "You are a business strategist with expertise in {industry} technologies. "
        "Develop a comprehensive strategy for {objective}, covering market "
        "analysis, competitive positioning, revenue models, risk mitigation, "
        "and KPIs."
    ),
    PromptCategory.CREATIVE: (
        "You are a creative writer and world-builder specializing in "
        "science-fiction and speculative technology. Create an engaging {format} "
        "about {topic} that entertains while educating readers about {concept}."
    ),
    PromptCategory.GENERAL: (
        "You are a knowledgeable assistant. Provide a clear, accurate, and "
        "helpful response about {topic}. Structure your answer with: "
        "(1) a brief overview, (2) key details, (3) practical examples, and "
        "(4) suggestions for further learning."
    ),
}

# Improvement strategies applied when refining a prompt
_IMPROVEMENT_STRATEGIES = [
    ("add_context", "Add relevant background context and constraints."),
    ("specify_format", "Specify the desired output format (e.g., bullet points, code, table)."),
    ("add_examples", "Include 1–3 concrete examples to anchor the request."),
    ("clarify_audience", "Explicitly state the target audience and their expertise level."),
    ("define_scope", "Narrow or expand the scope to match the desired level of detail."),
    ("add_constraints", "Add constraints such as length, tone, or specific terminology to avoid."),
    ("chain_of_thought", "Ask the model to reason step-by-step before providing an answer."),
    ("add_persona", "Assign a specific expert persona to shape the model's perspective."),
    ("request_alternatives", "Ask for multiple alternative approaches or perspectives."),
    ("verify_output", "Ask the model to verify its own answer for accuracy and completeness."),
]


class PromptEngineer:
    """
    Iterative prompt engineering system.

    Builds, improves, and manages prompts to extract the best possible
    responses from AI models across all domains in the encyclopedia.
    """

    def __init__(self) -> None:
        self._prompt_history: List[Prompt] = []

    # ------------------------------------------------------------------
    # Creating prompts
    # ------------------------------------------------------------------

    def create_from_template(
        self,
        category: PromptCategory,
        **kwargs: str,
    ) -> Prompt:
        """
        Create a prompt from a built-in template, filling in named placeholders.

        Example::

            engineer.create_from_template(
                PromptCategory.EDUCATIONAL,
                topic="Python",
                learner_type="robot",
                skill_level="beginner",
                concept="for loops",
            )
        """
        template = _TEMPLATES[category]
        try:
            text = template.format(**kwargs)
        except KeyError as exc:
            missing = str(exc).strip("'")
            raise ValueError(
                f"Template for '{category.value}' requires the placeholder {{{missing}}}. "
                f"Provide it as a keyword argument."
            ) from exc
        prompt = Prompt(text=text, category=category, tags=list(kwargs.keys()))
        self._prompt_history.append(prompt)
        return prompt

    def create_custom(self, text: str, category: PromptCategory, tags: Optional[List[str]] = None) -> Prompt:
        """Create a custom prompt from arbitrary text."""
        prompt = Prompt(text=text, category=category, tags=tags or [])
        self._prompt_history.append(prompt)
        return prompt

    # ------------------------------------------------------------------
    # Improving prompts
    # ------------------------------------------------------------------

    def improve(
        self,
        prompt: Prompt,
        strategies: Optional[List[str]] = None,
    ) -> Prompt:
        """
        Apply one or more improvement strategies to a prompt, returning
        a new (higher-version) prompt that is linked back to its parent.

        :param prompt: The prompt to improve.
        :param strategies: Names of strategies to apply. If None, all
            strategies are applied in order.
        :returns: An improved ``Prompt`` at version + 1.
        """
        available = {name: desc for name, desc in _IMPROVEMENT_STRATEGIES}
        if strategies is None:
            chosen = list(available.keys())
        else:
            unknown = set(strategies) - set(available.keys())
            if unknown:
                raise ValueError(
                    f"Unknown strategy name(s): {unknown}. "
                    f"Available: {list(available.keys())}"
                )
            chosen = strategies

        improvements = "\n".join(f"- {available[s]}" for s in chosen)
        new_text = (
            f"{prompt.text}\n\n"
            f"[Improvement notes applied]\n{improvements}"
        )

        improved = Prompt(
            text=new_text,
            category=prompt.category,
            version=prompt.version + 1,
            tags=list(prompt.tags),
            parent_prompt=prompt,
            improvement_notes=improvements,
        )
        self._prompt_history.append(improved)
        return improved

    def add_chain_of_thought(self, prompt: Prompt) -> Prompt:
        """
        Append a chain-of-thought instruction to a prompt, asking the model
        to reason step-by-step before answering.
        """
        new_text = (
            f"{prompt.text}\n\n"
            "Before providing your final answer, think through the problem "
            "step-by-step and show your reasoning."
        )
        improved = Prompt(
            text=new_text,
            category=prompt.category,
            version=prompt.version + 1,
            tags=prompt.tags + ["chain_of_thought"],
            parent_prompt=prompt,
            improvement_notes="Added chain-of-thought reasoning instruction.",
        )
        self._prompt_history.append(improved)
        return improved

    def add_few_shot_examples(self, prompt: Prompt, examples: List[Dict[str, str]]) -> Prompt:
        """
        Inject few-shot examples into a prompt.

        :param prompt: Base prompt to enhance.
        :param examples: List of dicts with ``"input"`` and ``"output"`` keys.
        """
        example_text = "\n\n".join(
            f"Example {i + 1}:\nInput: {ex['input']}\nOutput: {ex['output']}"
            for i, ex in enumerate(examples)
        )
        new_text = f"{prompt.text}\n\nHere are some examples:\n\n{example_text}"
        improved = Prompt(
            text=new_text,
            category=prompt.category,
            version=prompt.version + 1,
            tags=prompt.tags + ["few_shot"],
            parent_prompt=prompt,
            improvement_notes=f"Added {len(examples)} few-shot example(s).",
        )
        self._prompt_history.append(improved)
        return improved

    # ------------------------------------------------------------------
    # Inspection helpers
    # ------------------------------------------------------------------

    def list_strategies(self) -> List[Dict[str, str]]:
        """Return all available improvement strategies."""
        return [{"name": n, "description": d} for n, d in _IMPROVEMENT_STRATEGIES]

    def get_history(self) -> List[Prompt]:
        """Return all prompts created in this session."""
        return list(self._prompt_history)

    def get_lineage(self, prompt: Prompt) -> List[Prompt]:
        """
        Walk backwards through the parent chain and return the full
        lineage from the original prompt to the given one.
        """
        lineage: List[Prompt] = []
        current: Optional[Prompt] = prompt
        while current is not None:
            lineage.append(current)
            current = current.parent_prompt
        return list(reversed(lineage))

    def list_templates(self) -> List[str]:
        """Return category names for which built-in templates exist."""
        return [cat.value for cat in _TEMPLATES]
