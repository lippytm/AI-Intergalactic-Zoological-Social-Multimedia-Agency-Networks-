// Zig Starter — Comptime, error unions, allocators, structs, slices
// Run: zig run main.zig

const std = @import("std");
const Allocator = std.mem.Allocator;
const ArrayList = std.ArrayList;
const print = std.debug.print;

// ---------------------------------------------------------------------------
// Error set
// ---------------------------------------------------------------------------
const ZooError = error{
    NotFound,
    InvalidIntelligence,
    OutOfMemory,
};

// ---------------------------------------------------------------------------
// Struct
// ---------------------------------------------------------------------------
const Organism = struct {
    name:         []const u8,
    planet:       []const u8,
    intelligence: u8,

    pub fn init(name: []const u8, planet: []const u8, intelligence: u8) ZooError!Organism {
        if (intelligence > 100) return ZooError.InvalidIntelligence;
        return Organism{ .name = name, .planet = planet, .intelligence = intelligence };
    }

    pub fn describe(self: Organism) void {
        print("  {s} from {s} (IQ: {})\n", .{ self.name, self.planet, self.intelligence });
    }
};

// ---------------------------------------------------------------------------
// Comptime generic max
// ---------------------------------------------------------------------------
fn maxVal(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

// ---------------------------------------------------------------------------
// Fibonacci (comptime)
// ---------------------------------------------------------------------------
fn fibonacci(comptime n: u32) u64 {
    if (n <= 1) return n;
    return comptime fibonacci(n - 1) + fibonacci(n - 2);
}

// ---------------------------------------------------------------------------
// Sorting organisms by intelligence
// ---------------------------------------------------------------------------
fn compareIntelligence(_: void, a: Organism, b: Organism) bool {
    return a.intelligence > b.intelligence;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var list = ArrayList(Organism).init(allocator);
    defer list.deinit();

    const data = [_]struct { []const u8, []const u8, u8 }{
        .{ "Zorgon",  "Kepler-442b", 95 },
        .{ "Blorbax", "Gliese 667C", 72 },
        .{ "Floopix", "Proxima b",   88 },
        .{ "Grumbix", "HD 40307g",   61 },
    };

    for (data) |d| {
        const org = try Organism.init(d[0], d[1], d[2]);
        try list.append(org);
    }

    print("=== All Organisms ===\n", .{});
    for (list.items) |o| o.describe();

    // Sort by intelligence descending
    std.sort.pdq(Organism, list.items, {}, compareIntelligence);
    print("\n=== Top 2 by Intelligence ===\n", .{});
    for (list.items[0..2]) |o| o.describe();

    // Comptime fibonacci
    print("\n=== Fibonacci (comptime) ===\n", .{});
    inline for (.{ 0, 1, 2, 5, 10 }) |n| {
        print("  fib({}) = {}\n", .{ n, fibonacci(n) });
    }

    // Generic max
    print("\n=== Generic max ===\n", .{});
    print("  max(3, 7) = {}\n", .{ maxVal(i32, 3, 7) });
    print("  max(2.5, 1.1) = {d}\n", .{ maxVal(f64, 2.5, 1.1) });
}
