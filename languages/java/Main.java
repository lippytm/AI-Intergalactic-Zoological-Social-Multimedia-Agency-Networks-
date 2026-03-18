// Java Starter — Records, Sealed Classes, Pattern Matching, Streams, CompletableFuture
// Requires Java 21+

import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class Main {

    // -----------------------------------------------------------------------
    // Record
    // -----------------------------------------------------------------------
    record Planet(String name, double massKg, double radiusKm, List<String> moons) {
        double surfaceGravity() {
            final double G = 6.674e-11;
            double r = radiusKm * 1_000;
            return G * massKg / (r * r);
        }
    }

    // -----------------------------------------------------------------------
    // Sealed interface + pattern matching (Java 21)
    // -----------------------------------------------------------------------
    sealed interface Shape permits Circle, Rectangle, Triangle {}
    record Circle(double radius)                           implements Shape {}
    record Rectangle(double width, double height)          implements Shape {}
    record Triangle(double base, double height)            implements Shape {}

    static double area(Shape s) {
        return switch (s) {
            case Circle c       -> Math.PI * c.radius() * c.radius();
            case Rectangle r    -> r.width() * r.height();
            case Triangle t     -> 0.5 * t.base() * t.height();
        };
    }

    // -----------------------------------------------------------------------
    // Generic utility
    // -----------------------------------------------------------------------
    static <T extends Comparable<T>> Optional<T> max(List<T> list) {
        return list.stream().max(Comparator.naturalOrder());
    }

    // -----------------------------------------------------------------------
    // Stream pipeline
    // -----------------------------------------------------------------------
    static Map<String, Long> wordFrequency(String text) {
        return Arrays.stream(text.toLowerCase().split("\\W+"))
            .filter(w -> !w.isBlank())
            .collect(Collectors.groupingBy(w -> w, Collectors.counting()));
    }

    // -----------------------------------------------------------------------
    // Async with CompletableFuture
    // -----------------------------------------------------------------------
    static CompletableFuture<String> fetchPlanetInfo(String name) {
        return CompletableFuture.supplyAsync(() -> {
            try { Thread.sleep(50); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            return "Info about " + name;
        });
    }

    // -----------------------------------------------------------------------
    // Main
    // -----------------------------------------------------------------------
    public static void main(String[] args) throws Exception {
        var earth = new Planet("Earth", 5.972e24, 6_371, List.of("Moon"));
        System.out.printf("Surface gravity of %s: %.2f m/s²%n", earth.name(), earth.surfaceGravity());

        List<Shape> shapes = List.of(new Circle(5), new Rectangle(4, 6), new Triangle(3, 8));
        shapes.forEach(s -> System.out.printf("Area of %s: %.2f%n", s.getClass().getSimpleName(), area(s)));

        var nums = List.of(3, 1, 4, 1, 5, 9, 2, 6);
        System.out.println("Max: " + max(nums).orElse(-1));

        var freq = wordFrequency("the quick brown fox jumps over the lazy dog the fox");
        freq.entrySet().stream()
            .sorted(Map.Entry.<String, Long>comparingByValue().reversed())
            .limit(3)
            .forEach(e -> System.out.println(e.getKey() + " → " + e.getValue()));

        // Async
        var futures = List.of("Kepler-442b", "Proxima b", "Gliese 667Cc")
            .stream()
            .map(Main::fetchPlanetInfo)
            .toList();
        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
        futures.forEach(f -> System.out.println(f.join()));
    }
}
