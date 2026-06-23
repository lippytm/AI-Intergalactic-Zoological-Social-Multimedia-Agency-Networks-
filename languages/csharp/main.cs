// C# Starter — Records, Pattern Matching, LINQ, async/await, Nullable Reference Types
// .NET 8+  |  Run: dotnet script main.cs  OR  dotnet run

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

// ---------------------------------------------------------------------------
// Records
// ---------------------------------------------------------------------------
record Planet(string Name, double MassKg, double RadiusKm, IReadOnlyList<string> Moons)
{
    public double SurfaceGravity()
    {
        const double G = 6.674e-11;
        double r = RadiusKm * 1_000;
        return G * MassKg / (r * r);
    }
}

// ---------------------------------------------------------------------------
// Discriminated union via abstract record
// ---------------------------------------------------------------------------
abstract record Shape;
record Circle(double Radius) : Shape;
record Rectangle(double Width, double Height) : Shape;
record Triangle(double Base, double Height) : Shape;

static class ShapeExtensions
{
    public static double Area(this Shape s) => s switch
    {
        Circle c     => Math.PI * c.Radius * c.Radius,
        Rectangle r  => r.Width * r.Height,
        Triangle t   => 0.5 * t.Base * t.Height,
        _            => throw new ArgumentOutOfRangeException(nameof(s)),
    };
}

// ---------------------------------------------------------------------------
// Generic result type (Railway-Oriented Programming)
// ---------------------------------------------------------------------------
record Result<T>(T? Value, string? Error)
{
    public bool IsSuccess => Error is null;

    public static Result<T> Ok(T value) => new(value, null);
    public static Result<T> Fail(string error) => new(default, error);
}

// ---------------------------------------------------------------------------
// Async helpers
// ---------------------------------------------------------------------------
async Task<string> FetchDataAsync(string url)
{
    await Task.Delay(50);   // Simulate I/O
    return $"<data from {url}>";
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
var earth = new Planet("Earth", 5.972e24, 6_371, new[] { "Moon" });
Console.WriteLine($"Surface gravity of {earth.Name}: {earth.SurfaceGravity():F2} m/s²");

Shape[] shapes = { new Circle(5), new Rectangle(4, 6), new Triangle(3, 8) };
foreach (var s in shapes)
    Console.WriteLine($"Area of {s.GetType().Name}: {s.Area():F2}");

// LINQ pipeline
var numbers = Enumerable.Range(1, 20)
    .Where(n => n % 2 == 0)
    .Select(n => n * n)
    .Take(5)
    .ToList();
Console.WriteLine($"Even squares: {string.Join(", ", numbers)}");

// Pattern matching with switch
static string Classify(int n) => n switch
{
    < 0  => "negative",
    0    => "zero",
    < 10 => "small",
    _    => "large",
};
Console.WriteLine(string.Join(", ", new[] { -5, 0, 7, 42 }.Select(Classify)));

// Async
var tasks = new[] { "https://example.com", "https://example.org" }
    .Select(FetchDataAsync);
var results = await Task.WhenAll(tasks);
foreach (var r in results)
    Console.WriteLine(r);
