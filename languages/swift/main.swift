// Swift Starter — Protocols, Generics, Concurrency (async/await), Result, Property Wrappers
// Run: swift main.swift

import Foundation

// ---------------------------------------------------------------------------
// Protocol + extensions
// ---------------------------------------------------------------------------
protocol Describable {
    var description: String { get }
}

protocol Classifiable: Describable {
    var taxonomyClass: String { get }
}

// ---------------------------------------------------------------------------
// Generics
// ---------------------------------------------------------------------------
struct Registry<T: Describable> {
    private var items: [String: T] = [:]

    mutating func register(_ key: String, _ value: T) { items[key] = value }

    func lookup(_ key: String) -> T? { items[key] }

    var all: [T] { Array(items.values) }
}

// ---------------------------------------------------------------------------
// Enum with associated values
// ---------------------------------------------------------------------------
enum PlanetType {
    case rocky(distanceFromStar: Double)
    case gasGiant(rings: Int)
    case iceGiant
    case dwarf

    var humanReadable: String {
        switch self {
        case .rocky(let d):   return "Rocky planet, \(d) AU from star"
        case .gasGiant(let r): return "Gas giant with \(r) ring(s)"
        case .iceGiant:        return "Ice giant"
        case .dwarf:           return "Dwarf planet"
        }
    }
}

// ---------------------------------------------------------------------------
// Struct with property wrapper
// ---------------------------------------------------------------------------
@propertyWrapper
struct Clamped<T: Comparable> {
    var wrappedValue: T { didSet { wrappedValue = min(max(wrappedValue, lo), hi) } }
    let lo: T, hi: T
    init(wrappedValue: T, _ lo: T, _ hi: T) {
        self.lo = lo; self.hi = hi
        self.wrappedValue = min(max(wrappedValue, lo), hi)
    }
}

struct Organism: Classifiable {
    let name: String
    let planet: String
    @Clamped(0, 100) var intelligence: Int = 50

    var taxonomyClass: String { "ExtraterrestrialFauna" }
    var description: String { "\(name) from \(planet) (IQ: \(intelligence))" }
}

// ---------------------------------------------------------------------------
// Result & error handling
// ---------------------------------------------------------------------------
enum ZooError: Error, LocalizedError {
    case notFound(String)
    case invalidData

    var errorDescription: String? {
        switch self {
        case .notFound(let s): return "Not found: \(s)"
        case .invalidData:     return "Invalid data"
        }
    }
}

func findOrganism(named name: String, in registry: Registry<Organism>) -> Result<Organism, ZooError> {
    guard let org = registry.lookup(name) else { return .failure(.notFound(name)) }
    return .success(org)
}

// ---------------------------------------------------------------------------
// Async/await simulation (Swift 5.5+)
// ---------------------------------------------------------------------------
func fetchPlanetData(_ name: String) async -> String {
    try? await Task.sleep(nanoseconds: 50_000_000)
    return "Data for \(name)"
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
var reg = Registry<Organism>()
var zorgon = Organism(name: "Zorgon", planet: "Kepler-442b")
zorgon.intelligence = 95
reg.register("zorgon", zorgon)
reg.register("blorbax", Organism(name: "Blorbax", planet: "Gliese 667C"))

switch findOrganism(named: "zorgon", in: reg) {
case .success(let org): print("Found: \(org.description)")
case .failure(let err): print("Error: \(err.localizedDescription)")
}

switch findOrganism(named: "unknown", in: reg) {
case .success(let org): print("Found: \(org.description)")
case .failure(let err): print("Error: \(err.localizedDescription)")
}

let planets: [PlanetType] = [.rocky(distanceFromStar: 1.0), .gasGiant(rings: 2), .iceGiant, .dwarf]
planets.forEach { print($0.humanReadable) }
