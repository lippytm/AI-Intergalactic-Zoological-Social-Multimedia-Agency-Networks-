# Julia Starter — Multiple dispatch, macros, metaprogramming, async tasks
# Run: julia main.jl

# ---------------------------------------------------------------------------
# Struct + multiple dispatch
# ---------------------------------------------------------------------------
struct Planet
    name::String
    mass_kg::Float64
    radius_km::Float64
    moons::Vector{String}
end

Planet(name, mass, radius) = Planet(name, mass, radius, String[])

surface_gravity(p::Planet) = 6.674e-11 * p.mass_kg / (p.radius_km * 1e3)^2

Base.show(io::IO, p::Planet) =
    print(io, "Planet($(p.name), g≈$(round(surface_gravity(p), digits=2)) m/s²)")

# ---------------------------------------------------------------------------
# Abstract type hierarchy
# ---------------------------------------------------------------------------
abstract type Shape end

struct Circle    <: Shape; radius::Float64 end
struct Rectangle <: Shape; width::Float64; height::Float64 end
struct Triangle  <: Shape; base::Float64; height::Float64 end

area(s::Circle)    = π * s.radius^2
area(s::Rectangle) = s.width * s.height
area(s::Triangle)  = 0.5 * s.base * s.height

# ---------------------------------------------------------------------------
# Generic function + type parameter
# ---------------------------------------------------------------------------
function top_n(items::Vector{T}, n::Int, key::Function) where T
    sort(items, by=key, rev=true)[1:min(n, length(items))]
end

# ---------------------------------------------------------------------------
# Macro
# ---------------------------------------------------------------------------
macro timed_print(expr)
    quote
        t = @elapsed result = $(esc(expr))
        println("Result: $result  ($(round(t*1000, digits=3)) ms)")
        result
    end
end

# ---------------------------------------------------------------------------
# Async Tasks
# ---------------------------------------------------------------------------
function fetch_data(source::String)
    sleep(0.05)
    "Data from $source"
end

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
planets = [
    Planet("Earth",   5.972e24, 6_371.0, ["Moon"]),
    Planet("Jupiter", 1.898e27, 69_911.0),
    Planet("Mars",    6.417e23, 3_389.5,  ["Phobos", "Deimos"]),
]

println("=== Planets ===")
for p in planets
    println("  ", p)
end

shapes = [Circle(5.0), Rectangle(4.0, 6.0), Triangle(3.0, 8.0)]
println("\n=== Shapes ===")
for s in shapes
    println("  $(typeof(s)) area = $(round(area(s), digits=3))")
end

println("\n=== Top 2 planets by mass ===")
for p in top_n(planets, 2, p -> p.mass_kg)
    println("  ", p.name)
end

println("\n=== Macro timing ===")
@timed_print sum(1:1_000_000)

println("\n=== Async tasks ===")
tasks = [@async fetch_data("source-$i") for i in 1:3]
results = fetch.(tasks)
foreach(println, results)
