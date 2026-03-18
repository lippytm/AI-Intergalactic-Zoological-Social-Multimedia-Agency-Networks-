// TypeScript Starter — Generics, Decorators, Utility Types, Mapped Types
// tsconfig: {"strict": true, "target": "ES2022", "experimentalDecorators": true}

// ---------------------------------------------------------------------------
// Generics & constraints
// ---------------------------------------------------------------------------
interface Identifiable {
  id: string;
}

function findById<T extends Identifiable>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}

// ---------------------------------------------------------------------------
// Mapped types & conditional types
// ---------------------------------------------------------------------------
type ReadOnly<T> = { readonly [K in keyof T]: T[K] };
type Optional<T> = { [K in keyof T]?: T[K] };
type NonNullable2<T> = T extends null | undefined ? never : T;

// ---------------------------------------------------------------------------
// Discriminated unions
// ---------------------------------------------------------------------------
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":      return Math.PI * shape.radius ** 2;
    case "rectangle":   return shape.width * shape.height;
    case "triangle":    return 0.5 * shape.base * shape.height;
  }
}

// ---------------------------------------------------------------------------
// Async + type-safe fetch wrapper
// ---------------------------------------------------------------------------
async function typedFetch<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json() as Promise<T>;
}

// ---------------------------------------------------------------------------
// Decorator (method timing)
// ---------------------------------------------------------------------------
function timed(_target: unknown, key: string, descriptor: PropertyDescriptor) {
  const original = descriptor.value as (...args: unknown[]) => unknown;
  descriptor.value = function (...args: unknown[]) {
    const start = performance.now();
    const result = original.apply(this, args);
    console.log(`${key} took ${(performance.now() - start).toFixed(2)}ms`);
    return result;
  };
  return descriptor;
}

class MathEngine {
  @timed
  factorial(n: number): bigint {
    if (n <= 1) return 1n;
    return BigInt(n) * this.factorial(n - 1);
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
const circle: Shape = { kind: "circle", radius: 5 };
const rect: Shape   = { kind: "rectangle", width: 4, height: 6 };
console.log(`Circle area: ${area(circle).toFixed(2)}`);
console.log(`Rectangle area: ${area(rect)}`);

const engine = new MathEngine();
console.log(`10! = ${engine.factorial(10)}`);
