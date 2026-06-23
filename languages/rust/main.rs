// Rust Starter — Ownership, Traits, Generics, Async, Error Handling
// Run: cargo run

use std::fmt;
use std::collections::HashMap;

// ---------------------------------------------------------------------------
// Custom trait
// ---------------------------------------------------------------------------
trait Describe {
    fn describe(&self) -> String;
}

// ---------------------------------------------------------------------------
// Generic struct with trait bounds
// ---------------------------------------------------------------------------
#[derive(Debug, Clone)]
struct Registry<T: Describe + Clone> {
    items: HashMap<String, T>,
}

impl<T: Describe + Clone> Registry<T> {
    fn new() -> Self {
        Registry { items: HashMap::new() }
    }

    fn insert(&mut self, key: impl Into<String>, value: T) {
        self.items.insert(key.into(), value);
    }

    fn get(&self, key: &str) -> Option<&T> {
        self.items.get(key)
    }

    fn describe_all(&self) {
        for (k, v) in &self.items {
            println!("[{}] {}", k, v.describe());
        }
    }
}

// ---------------------------------------------------------------------------
// Concrete type
// ---------------------------------------------------------------------------
#[derive(Debug, Clone)]
struct Organism {
    name: String,
    planet: String,
    intelligence: u8, // 0–100
}

impl Describe for Organism {
    fn describe(&self) -> String {
        format!(
            "{} from {} (intelligence: {})",
            self.name, self.planet, self.intelligence
        )
    }
}

impl fmt::Display for Organism {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.describe())
    }
}

// ---------------------------------------------------------------------------
// Error handling with Result
// ---------------------------------------------------------------------------
#[derive(Debug)]
enum ZooError {
    NotFound(String),
    InvalidIntelligence(u8),
}

impl fmt::Display for ZooError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ZooError::NotFound(n) => write!(f, "Organism not found: {}", n),
            ZooError::InvalidIntelligence(v) => write!(f, "Intelligence {} out of range 0–100", v),
        }
    }
}

fn create_organism(name: &str, planet: &str, intelligence: u8) -> Result<Organism, ZooError> {
    if intelligence > 100 {
        return Err(ZooError::InvalidIntelligence(intelligence));
    }
    Ok(Organism {
        name: name.to_string(),
        planet: planet.to_string(),
        intelligence,
    })
}

// ---------------------------------------------------------------------------
// Iterator adaptors
// ---------------------------------------------------------------------------
fn top_intelligent(organisms: &[Organism], n: usize) -> Vec<&Organism> {
    let mut sorted: Vec<&Organism> = organisms.iter().collect();
    sorted.sort_by(|a, b| b.intelligence.cmp(&a.intelligence));
    sorted.into_iter().take(n).collect()
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
fn main() {
    let mut registry: Registry<Organism> = Registry::new();

    let beings = vec![
        ("zorgon",  "Kepler-442b", 95u8),
        ("blorbax", "Gliese 667C", 72),
        ("floopix", "Proxima b",   88),
        ("grumbix", "HD 40307g",   61),
    ];

    for (name, planet, intel) in beings {
        match create_organism(name, planet, intel) {
            Ok(org) => registry.insert(name, org),
            Err(e)  => eprintln!("Error creating organism: {}", e),
        }
    }

    println!("=== All Organisms ===");
    registry.describe_all();

    let all: Vec<Organism> = registry.items.values().cloned().collect();
    println!("\n=== Top 2 by Intelligence ===");
    for org in top_intelligent(&all, 2) {
        println!("{}", org);
    }

    // Pattern matching with Option
    match registry.get("zorgon") {
        Some(org) => println!("\nFound: {}", org),
        None => println!("\nNot found"),
    }
}
