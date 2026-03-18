// JavaScript Starter — Modern ES2024 Features
// Covers: classes, async/await, generators, Proxy, WeakRef, structuredClone

"use strict";

// ---------------------------------------------------------------------------
// Classes & private fields
// ---------------------------------------------------------------------------
class SpaceCreature {
  #id;
  #genome;

  constructor(id, species, genome = []) {
    this.#id = id;
    this.species = species;
    this.#genome = genome;
  }

  get id() { return this.#id; }

  mutate(gene) {
    this.#genome = [...this.#genome, gene];
    return this;
  }

  toJSON() {
    return { id: this.#id, species: this.species, genomeLength: this.#genome.length };
  }
}

// ---------------------------------------------------------------------------
// Async / await + Promise.allSettled
// ---------------------------------------------------------------------------
async function fetchPlanetData(planetName) {
  // Simulate network latency
  await new Promise(resolve => setTimeout(resolve, 50));
  return { planet: planetName, population: Math.floor(Math.random() * 1e9) };
}

async function fetchAllPlanets(names) {
  const results = await Promise.allSettled(names.map(fetchPlanetData));
  return results.map(r => (r.status === "fulfilled" ? r.value : { error: r.reason }));
}

// ---------------------------------------------------------------------------
// Generator
// ---------------------------------------------------------------------------
function* idGenerator(prefix = "ID") {
  let n = 0;
  while (true) yield `${prefix}-${String(++n).padStart(6, "0")}`;
}

// ---------------------------------------------------------------------------
// Functional utilities
// ---------------------------------------------------------------------------
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x);

const double = x => x * 2;
const addTen = x => x + 10;
const square = x => x ** 2;

const transform = pipe(double, addTen, square);

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
(async () => {
  const creature = new SpaceCreature(1, "Zorgon");
  creature.mutate("ATCG").mutate("GCTA");
  console.log("Creature:", JSON.stringify(creature.toJSON()));

  const planets = await fetchAllPlanets(["Kepler-442b", "Proxima Centauri b", "Gliese 667Cc"]);
  console.log("Planets:", planets);

  const gen = idGenerator("CREATURE");
  console.log("Generated IDs:", [gen.next().value, gen.next().value, gen.next().value]);

  console.log("Transform(5):", transform(5)); // ((5*2)+10)^2 = 400
})();
