-- Lua Starter — Metatables, Coroutines, OOP, functional patterns
-- Run: lua main.lua

-- ---------------------------------------------------------------------------
-- OOP via metatables
-- ---------------------------------------------------------------------------
local Organism = {}
Organism.__index = Organism

function Organism.new(name, planet, intelligence)
    local self = setmetatable({}, Organism)
    self.name         = name
    self.planet       = planet
    self.intelligence = math.max(0, math.min(100, intelligence))
    return self
end

function Organism:describe()
    return string.format("Organism(%s, %s, IQ=%d)", self.name, self.planet, self.intelligence)
end

function Organism:__tostring() return self:describe() end

-- ---------------------------------------------------------------------------
-- Coroutine-based generator
-- ---------------------------------------------------------------------------
local function fibonacci()
    return coroutine.wrap(function()
        local a, b = 0, 1
        while true do
            coroutine.yield(a)
            a, b = b, a + b
        end
    end)
end

-- ---------------------------------------------------------------------------
-- Functional helpers
-- ---------------------------------------------------------------------------
local function map(t, fn)
    local result = {}
    for i, v in ipairs(t) do result[i] = fn(v) end
    return result
end

local function filter(t, fn)
    local result = {}
    for _, v in ipairs(t) do
        if fn(v) then result[#result + 1] = v end
    end
    return result
end

local function reduce(t, fn, acc)
    for _, v in ipairs(t) do acc = fn(acc, v) end
    return acc
end

-- ---------------------------------------------------------------------------
-- Main
-- ---------------------------------------------------------------------------
local organisms = {
    Organism.new("Zorgon",  "Kepler-442b", 95),
    Organism.new("Blorbax", "Gliese 667C", 72),
    Organism.new("Floopix", "Proxima b",   88),
    Organism.new("Grumbix", "HD 40307g",   61),
}

print("=== All organisms ===")
for _, o in ipairs(organisms) do print("  " .. tostring(o)) end

local high_iq = filter(organisms, function(o) return o.intelligence >= 80 end)
print(string.format("\nHigh-IQ count: %d", #high_iq))

local total = reduce(map(organisms, function(o) return o.intelligence end), function(a, b) return a + b end, 0)
print(string.format("Total IQ: %d", total))

print("\nFibonacci:")
local fib = fibonacci()
local seq = {}
for _ = 1, 10 do seq[#seq + 1] = fib() end
print(table.concat(seq, ", "))

-- Closure counter
local function make_counter(start)
    local count = start or 0
    return {
        increment = function() count = count + 1 end,
        get       = function() return count end,
    }
end

local c = make_counter(10)
c.increment(); c.increment()
print(string.format("\nCounter: %d", c.get()))
