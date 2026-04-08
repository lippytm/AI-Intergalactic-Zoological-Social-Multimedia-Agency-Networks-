// Scala 3 Starter — Case classes, Enums, Type classes, For comprehensions, Futures
// Run: scala main.scala  OR  sbt run

import scala.concurrent.{Await, Future}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration.*
import scala.util.{Failure, Success, Try}

// ---------------------------------------------------------------------------
// Case classes & companion objects
// ---------------------------------------------------------------------------
case class Planet(name: String, massKg: Double, radiusKm: Double, moons: List[String] = Nil):
  def surfaceGravity: Double =
    val G = 6.674e-11
    val r = radiusKm * 1_000
    G * massKg / (r * r)

// ---------------------------------------------------------------------------
// Enum (Scala 3)
// ---------------------------------------------------------------------------
enum PlanetType:
  case Rocky, GasGiant, IceGiant, Dwarf

// ---------------------------------------------------------------------------
// Type class pattern
// ---------------------------------------------------------------------------
trait Show[A]:
  def show(a: A): String

given Show[Planet] with
  def show(p: Planet): String = s"${p.name} (moons: ${p.moons.mkString(", ")})"

def display[A: Show](a: A): String = summon[Show[A]].show(a)

// ---------------------------------------------------------------------------
// For comprehension + Option
// ---------------------------------------------------------------------------
def safeDivide(a: Double, b: Double): Option[Double] =
  if b == 0 then None else Some(a / b)

def computation(x: Double, y: Double, z: Double): Option[Double] =
  for
    a <- safeDivide(x, y)
    b <- safeDivide(a, z)
  yield b

// ---------------------------------------------------------------------------
// Futures
// ---------------------------------------------------------------------------
def fetchPlanetData(name: String): Future[String] = Future:
  Thread.sleep(50)
  s"Data for $name"

// ---------------------------------------------------------------------------
// Higher-order functions
// ---------------------------------------------------------------------------
extension [A](list: List[A])
  def groupByPredicate(p: A => Boolean): (List[A], List[A]) = list.partition(p)

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
@main def run(): Unit =
  val earth = Planet("Earth", 5.972e24, 6_371.0, List("Moon"))
  println(f"Surface gravity of ${earth.name}: ${earth.surfaceGravity}%.2f m/s²")
  println(display(earth))

  println(computation(100, 4, 5))   // Some(5.0)
  println(computation(100, 0, 5))   // None

  val planets = List("Kepler-442b", "Proxima b", "Gliese 667Cc")
  val future = Future.sequence(planets.map(fetchPlanetData))
  val results = Await.result(future, 5.seconds)
  results.foreach(println)

  val nums = (1 to 20).toList
  val (evens, odds) = nums.groupByPredicate(_ % 2 == 0)
  println(s"Evens: ${evens.take(5)}")
  println(s"Odds:  ${odds.take(5)}")
