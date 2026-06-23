// Kotlin Starter — Data classes, Sealed classes, Coroutines, Extension functions, DSL
// Run: kotlinc main.kt -include-runtime -d main.jar && java -jar main.jar

import kotlinx.coroutines.*

// ---------------------------------------------------------------------------
// Data classes
// ---------------------------------------------------------------------------
data class Planet(
    val name: String,
    val massKg: Double,
    val radiusKm: Double,
    val moons: List<String> = emptyList()
) {
    fun surfaceGravity(): Double {
        val G = 6.674e-11
        val r = radiusKm * 1_000
        return G * massKg / (r * r)
    }
}

// ---------------------------------------------------------------------------
// Sealed class hierarchy
// ---------------------------------------------------------------------------
sealed class Shape {
    abstract fun area(): Double
}
data class Circle(val radius: Double)              : Shape() { override fun area() = Math.PI * radius * radius }
data class Rectangle(val w: Double, val h: Double) : Shape() { override fun area() = w * h }
data class Triangle(val base: Double, val ht: Double) : Shape() { override fun area() = 0.5 * base * ht }

// ---------------------------------------------------------------------------
// Extension functions
// ---------------------------------------------------------------------------
fun Double.roundTo(n: Int): Double {
    val factor = Math.pow(10.0, n.toDouble())
    return Math.round(this * factor) / factor
}

fun <T> List<T>.second(): T = this[1]

// ---------------------------------------------------------------------------
// Type-safe builder DSL
// ---------------------------------------------------------------------------
class ZooBuilder {
    val organisms = mutableListOf<String>()
    fun organism(name: String, planet: String) { organisms += "$name ($planet)" }
    fun build() = organisms.toList()
}

fun zoo(block: ZooBuilder.() -> Unit) = ZooBuilder().apply(block).build()

// ---------------------------------------------------------------------------
// Coroutines
// ---------------------------------------------------------------------------
suspend fun fetchData(source: String): String {
    delay(50)
    return "Data from $source"
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
fun main() = runBlocking {
    val earth = Planet("Earth", 5.972e24, 6_371.0, listOf("Moon"))
    println("Surface gravity of ${earth.name}: ${earth.surfaceGravity().roundTo(2)} m/s²")

    val shapes: List<Shape> = listOf(Circle(5.0), Rectangle(4.0, 6.0), Triangle(3.0, 8.0))
    shapes.forEach { println("Area of ${it::class.simpleName}: ${it.area().roundTo(2)}") }

    val inhabitants = zoo {
        organism("Zorgon",  "Kepler-442b")
        organism("Blorbax", "Gliese 667C")
        organism("Floopix", "Proxima b")
    }
    println("\nZoo inhabitants:")
    inhabitants.forEach { println("  $it") }

    // Coroutines
    val results = (1..3).map { i ->
        async { fetchData("source-$i") }
    }.awaitAll()
    println("\nAsync results: $results")
}
