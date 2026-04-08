<?php
// PHP Starter — OOP, Traits, Generators, Fibers (PHP 8.1+), named arguments
// Run: php main.php

declare(strict_types=1);

// ---------------------------------------------------------------------------
// Trait
// ---------------------------------------------------------------------------
trait Describable
{
    public function describe(): string
    {
        $props = get_object_vars($this);
        $parts = array_map(fn($k, $v) => "$k=$v", array_keys($props), $props);
        return static::class . '(' . implode(', ', $parts) . ')';
    }
}

// ---------------------------------------------------------------------------
// Abstract class + interface
// ---------------------------------------------------------------------------
interface Shape
{
    public function area(): float;
}

abstract class BaseOrganism
{
    use Describable;

    public function __construct(
        public readonly string $name,
        public readonly string $planet,
        public readonly int    $intelligence,
    ) {}
}

// ---------------------------------------------------------------------------
// Concrete implementations
// ---------------------------------------------------------------------------
class Organism extends BaseOrganism {}

class Circle implements Shape
{
    public function __construct(private float $radius) {}
    public function area(): float { return M_PI * $this->radius ** 2; }
}

class Rectangle implements Shape
{
    public function __construct(private float $w, private float $h) {}
    public function area(): float { return $this->w * $this->h; }
}

// ---------------------------------------------------------------------------
// Generator
// ---------------------------------------------------------------------------
function fibonacci(): Generator
{
    [$a, $b] = [0, 1];
    while (true) {
        yield $a;
        [$a, $b] = [$b, $a + $b];
    }
}

// ---------------------------------------------------------------------------
// Fiber (PHP 8.1)
// ---------------------------------------------------------------------------
$fiber = new Fiber(function (): void {
    $value = Fiber::suspend('first');
    echo "Fiber received: $value\n";
    Fiber::suspend('second');
});

// ---------------------------------------------------------------------------
// Enum (PHP 8.1)
// ---------------------------------------------------------------------------
enum PlanetType: string
{
    case Rocky    = 'rocky';
    case GasGiant = 'gas_giant';
    case IceGiant = 'ice_giant';
    case Dwarf    = 'dwarf';
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
$organisms = [
    new Organism(name: 'Zorgon',  planet: 'Kepler-442b', intelligence: 95),
    new Organism(name: 'Blorbax', planet: 'Gliese 667C', intelligence: 72),
    new Organism(name: 'Floopix', planet: 'Proxima b',   intelligence: 88),
];

echo "=== Organisms ===\n";
foreach ($organisms as $o) {
    echo '  ' . $o->describe() . PHP_EOL;
}

usort($organisms, fn($a, $b) => $b->intelligence <=> $a->intelligence);
echo "\nTop organism: {$organisms[0]->name}\n";

echo "\n=== Shapes ===\n";
$shapes = [new Circle(5.0), new Rectangle(4.0, 6.0)];
foreach ($shapes as $s) {
    printf("  %s area = %.2f\n", $s::class, $s->area());
}

echo "\n=== Fibonacci ===\n";
$gen = fibonacci();
$fibs = [];
for ($i = 0; $i < 10; $i++, $gen->next()) {
    $fibs[] = $gen->current();
}
echo implode(', ', $fibs) . PHP_EOL;

echo "\n=== Fiber ===\n";
$v1 = $fiber->start();
echo "Fiber suspended with: $v1\n";
$v2 = $fiber->resume('hello');
echo "Fiber suspended with: $v2\n";

echo "\n=== Enum ===\n";
echo PlanetType::GasGiant->value . PHP_EOL;
