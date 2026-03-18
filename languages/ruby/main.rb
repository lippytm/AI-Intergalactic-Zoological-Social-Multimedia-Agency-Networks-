# Ruby Starter — Classes, Modules, Blocks, Fibers, Pattern Matching (Ruby 3+)
# Run: ruby main.rb

# frozen_string_literal: true

require 'json'
require 'ostruct'

# ---------------------------------------------------------------------------
# Module mixin
# ---------------------------------------------------------------------------
module Describable
  def describe
    vars = instance_variables.map { |v| "#{v.to_s.delete('@')}=#{instance_variable_get(v).inspect}" }
    "#{self.class.name}(#{vars.join(', ')})"
  end
end

# ---------------------------------------------------------------------------
# Class hierarchy
# ---------------------------------------------------------------------------
class Organism
  include Describable
  include Comparable

  attr_reader :name, :planet, :intelligence

  def initialize(name, planet, intelligence)
    @name         = name
    @planet       = planet
    @intelligence = intelligence.clamp(0, 100)
  end

  def <=>(other)
    intelligence <=> other.intelligence
  end

  def to_h
    { name:, planet:, intelligence: }
  end
end

# ---------------------------------------------------------------------------
# Enumerable + blocks
# ---------------------------------------------------------------------------
class Zoo
  include Enumerable

  def initialize
    @organisms = []
  end

  def add(org) = tap { @organisms << org }

  def each(&block) = @organisms.each(&block)

  def top(n) = sort.last(n).reverse
end

# ---------------------------------------------------------------------------
# Fiber-based generator
# ---------------------------------------------------------------------------
def fibonacci_fiber
  Fiber.new do
    a, b = 0, 1
    loop do
      Fiber.yield a
      a, b = b, a + b
    end
  end
end

# ---------------------------------------------------------------------------
# Pattern matching (Ruby 3+)
# ---------------------------------------------------------------------------
def classify_reading(reading)
  case reading
  in { sensor: 'temperature', value: (..0) }          then 'below freezing'
  in { sensor: 'temperature', value: (0..37) }        then 'normal range'
  in { sensor: 'temperature', value: (37..) }         then 'overheating'
  in { sensor: 'radiation',   value: (100..) }        then 'danger: high radiation'
  in { sensor: String => s }                           then "unknown sensor: #{s}"
  end
end

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
zoo = Zoo.new
zoo.add(Organism.new('Zorgon',  'Kepler-442b', 95))
   .add(Organism.new('Blorbax', 'Gliese 667C', 72))
   .add(Organism.new('Floopix', 'Proxima b',   88))

puts 'All organisms:'
zoo.each { |o| puts "  #{o.describe}" }

puts "\nTop 2 by intelligence:"
zoo.top(2).each { |o| puts "  #{o.name} (#{o.intelligence})" }

puts "\nFibonacci:"
fib = fibonacci_fiber
puts Array.new(10) { fib.resume }.inspect

puts "\nPattern matching:"
readings = [
  { sensor: 'temperature', value: -5 },
  { sensor: 'temperature', value: 22 },
  { sensor: 'radiation',   value: 150 },
]
readings.each { |r| puts "  #{r} → #{classify_reading(r)}" }

puts "\nJSON round-trip:"
data = zoo.map(&:to_h).to_json
puts JSON.parse(data).map { |h| h['name'] }.inspect
