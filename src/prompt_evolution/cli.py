"""Command-line interface for the evolutionary prompt engineering framework.

Usage
-----
::

    # Evolve from a built-in template
    python -m prompt_evolution --template zoo_catalog

    # Evolve from a custom seed prompt
    python -m prompt_evolution --seed "Describe alien ecosystems."

    # Full options
    python -m prompt_evolution --seed "My prompt." \\
        --population 12 --generations 8 --mutation-rate 0.7 \\
        --elite 2 --tournament 3 --seed-val 42 --verbose
"""

from __future__ import annotations

import argparse
import sys

from .evolver import PromptEvolver
from .templates import PROMPT_TEMPLATES


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prompt_evolution",
        description=(
            "Evolutionary Prompt Engineering — evolve prompts toward higher "
            "quality through selection, mutation, and crossover."
        ),
    )

    seed_group = parser.add_mutually_exclusive_group(required=True)
    seed_group.add_argument(
        "--seed",
        metavar="PROMPT",
        help="Custom seed prompt text.",
    )
    seed_group.add_argument(
        "--template",
        metavar="NAME",
        choices=sorted(PROMPT_TEMPLATES.keys()),
        help="Use a built-in template as the seed prompt.",
    )
    seed_group.add_argument(
        "--list-templates",
        action="store_true",
        default=False,
        help="List all available template names and exit.",
    )

    parser.add_argument(
        "--population",
        type=int,
        default=8,
        metavar="N",
        help="Population size per generation (default: 8).",
    )
    parser.add_argument(
        "--generations",
        type=int,
        default=5,
        metavar="N",
        help="Number of evolutionary generations (default: 5).",
    )
    parser.add_argument(
        "--mutation-rate",
        type=float,
        default=0.6,
        metavar="RATE",
        help="Probability of mutation vs crossover (default: 0.6).",
    )
    parser.add_argument(
        "--elite",
        type=int,
        default=2,
        metavar="N",
        help="Number of elite prompts carried forward each generation (default: 2).",
    )
    parser.add_argument(
        "--tournament",
        type=int,
        default=3,
        metavar="K",
        help="Tournament selection size (default: 3).",
    )
    parser.add_argument(
        "--seed-val",
        type=int,
        default=None,
        metavar="INT",
        help="Random seed for reproducibility.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Print fitness statistics after each generation.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=3,
        metavar="N",
        help="Display the top N evolved prompts (default: 3).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_templates:
        print("Available templates:")
        for name, text in sorted(PROMPT_TEMPLATES.items()):
            preview = text[:80].replace("\n", " ")
            print(f"  {name:<25} — {preview}…")
        return 0

    if args.template:
        seed_text = PROMPT_TEMPLATES[args.template]
    else:
        seed_text = args.seed

    evolver = PromptEvolver(
        population_size=args.population,
        generations=args.generations,
        mutation_rate=args.mutation_rate,
        elite_size=args.elite,
        tournament_k=args.tournament,
        seed=args.seed_val,
        verbose=args.verbose,
    )

    print(f"\n{'='*60}")
    print("  Evolutionary Prompt Engineering")
    print(f"{'='*60}")
    print(f"  Seed : {seed_text[:80]}{'…' if len(seed_text) > 80 else ''}")
    print(f"  Gens : {args.generations}  |  Pop : {args.population}  |  "
          f"Mutation rate : {args.mutation_rate}")
    print(f"{'='*60}\n")

    best = evolver.evolve([seed_text])

    # Show top-k results
    last_pop = evolver.history[-1]
    top_prompts = last_pop.top_k(args.top)

    print(f"\n{'─'*60}")
    print(f"  Top {args.top} evolved prompts (final generation)")
    print(f"{'─'*60}")
    for rank, p in enumerate(top_prompts, start=1):
        print(f"\n  [{rank}] Fitness: {p.fitness:.4f}  |  Gen: {p.generation}")
        print(f"  {p.text}")

    print(f"\n{'─'*60}")
    print("  Overall best prompt")
    print(f"{'─'*60}")
    print(f"\n  Fitness : {best.fitness:.4f}")
    print(f"  Gen     : {best.generation}")
    print(f"\n  {best.text}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
