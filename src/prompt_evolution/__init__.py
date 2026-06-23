"""
prompt_evolution — Evolutionary Prompt Engineering Framework

Applies evolutionary algorithm concepts (selection, mutation, crossover)
to iteratively build, refine, and evolve AI prompts toward higher quality.
"""

from .prompt import Prompt
from .population import PromptPopulation
from .operators import mutate, crossover, tournament_select
from .fitness import score_prompt
from .evolver import PromptEvolver
from .templates import PROMPT_TEMPLATES

__all__ = [
    "Prompt",
    "PromptPopulation",
    "mutate",
    "crossover",
    "tournament_select",
    "score_prompt",
    "PromptEvolver",
    "PROMPT_TEMPLATES",
]
