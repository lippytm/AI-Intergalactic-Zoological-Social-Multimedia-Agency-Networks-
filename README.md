# AI Intergalactic Zoological Social Multimedia Agency Networks

> The Space Aliens Social Political Party Networks of the Intergalactic Zoological Society Systems Networks of the Quantum Entanglements of the Many Worlds Networks of Time Machines Managements Systems

---

## Evolutionary Prompt Engineering Framework

**Prompts building better prompts.**

This repository contains `prompt_evolution`, a Python framework that applies **evolutionary algorithm** concepts — selection, mutation, crossover, and fitness evaluation — to iteratively improve AI prompts.  The result is a fully automated pipeline that breeds progressively higher-quality prompts from a simple seed text.

### How it works

```
Seed Prompts
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│  Generation 0: Initialise population from seed prompts      │
│  ↓  Evaluate fitness (clarity, specificity, structure …)    │
│  ↓  Tournament selection → pick best parents                │
│  ↓  Mutate (append clause / prepend role / insert context …)│
│  ↓  Crossover (sentence splice / phrase splice)             │
│  ↓  Elitism: keep top N prompts                             │
│  ↓  Repeat for N generations                                │
│  ↓  Return overall best prompt                              │
└─────────────────────────────────────────────────────────────┘
```

### Evolutionary operators

| Operator | Description |
|---|---|
| `mutate` – *append_clause* | Appends a refining instruction clause |
| `mutate` – *prepend_role* | Prepends a role-framing statement |
| `mutate` – *substitute_verb* | Replaces a generic verb with an instructional one |
| `mutate` – *insert_context* | Inserts a domain-context sentence mid-prompt |
| `crossover` – *sentence_crossover* | Interleaves sentences from two parent prompts |
| `crossover` – *phrase_splice* | Joins the first half of one prompt with the second half of another |
| `tournament_select` | Picks the fittest prompt from a random sub-group |

### Fitness scoring

Prompts are scored 0–1 across five heuristic dimensions:

1. **Clarity** — optimal length (50–500 characters)
2. **Specificity** — presence of instructional keywords (`explain`, `create`, `evolve` …)
3. **Structure** — punctuation, numbering, line breaks
4. **Diversity** — character-level Shannon entropy
5. **Role framing** — does the prompt set a clear actor/context?

> In production, replace `score_prompt` with a real LLM evaluator by passing a `fitness_fn` to `PromptEvolver`.

---

## Quick start

### Install

```bash
pip install -e .
```

### Evolve a custom prompt

```bash
python -m prompt_evolution --seed "Describe alien ecosystems." --verbose
```

### Evolve from a built-in template

```bash
python -m prompt_evolution --template zoo_catalog --generations 8 --verbose
```

### List all built-in templates

```bash
python -m prompt_evolution --list-templates
```

### Python API

```python
from prompt_evolution import PromptEvolver

evolver = PromptEvolver(
    population_size=10,
    generations=5,
    mutation_rate=0.6,
    seed=42,
    verbose=True,
)

best = evolver.evolve(["Describe the intergalactic zoo."])
print(best.text)
print(f"Fitness: {best.fitness:.4f}")
```

---

## Package structure

```
src/prompt_evolution/
├── __init__.py       Public API
├── prompt.py         Prompt dataclass
├── population.py     PromptPopulation collection
├── fitness.py        Heuristic fitness scoring
├── operators.py      Mutation, crossover, selection
├── evolver.py        PromptEvolver orchestrator
├── templates.py      Curated seed prompt library
└── cli.py            Command-line interface

tests/
├── test_prompt.py
├── test_fitness.py
├── test_operators.py
├── test_population.py
└── test_evolver.py
```

## Running tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Built-in prompt templates

| Template key | Theme |
|---|---|
| `prompt_meta` | Meta-prompt for generating intergalactic prompts |
| `prompt_refine` | Refine a draft prompt |
| `prompt_evolve` | Generate evolved variants of a prompt |
| `zoo_catalog` | Catalogue of alien species (xenobiology) |
| `zoo_ethics` | Ethics policy for the Zoological Society |
| `quantum_narrative` | Multi-universe quantum-entanglement story |
| `quantum_teaching` | Teaching quantum physics to space aliens |
| `ai_teacher` | ML curriculum for interspecies learners |
| `robotics_wearable` | Wearable AI exosuit design |
| `blockchain_basics` | Blockchain intro for beginners / aliens |
| `blockchain_advanced` | Decentralised governance for the Zoological Society |
| `time_management` | Protocols for the Time Machines Management System |
| `political_manifesto` | Space Aliens Social Political Party manifesto |
| `evolutionary_loop` | Full meta-evolutionary prompting loop |

---

## License

MIT

