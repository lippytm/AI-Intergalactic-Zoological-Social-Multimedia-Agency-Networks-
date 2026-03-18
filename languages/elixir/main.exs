# Elixir Starter — Pattern matching, Processes, GenServer, Pipes, Protocols
# Run: elixir main.exs

# ---------------------------------------------------------------------------
# Structs + Protocols
# ---------------------------------------------------------------------------
defmodule Organism do
  defstruct [:name, :planet, intelligence: 50]

  def new(name, planet, intelligence) do
    %__MODULE__{name: name, planet: planet, intelligence: min(max(intelligence, 0), 100)}
  end
end

defprotocol Describable do
  def describe(entity)
end

defimpl Describable, for: Organism do
  def describe(%Organism{name: n, planet: p, intelligence: iq}) do
    "#{n} from #{p} (IQ: #{iq})"
  end
end

# ---------------------------------------------------------------------------
# Pattern matching + recursion
# ---------------------------------------------------------------------------
defmodule Math do
  def fibonacci(0), do: 0
  def fibonacci(1), do: 1
  def fibonacci(n) when n > 1, do: fibonacci(n - 1) + fibonacci(n - 2)

  def factorial(0), do: 1
  def factorial(n) when n > 0, do: n * factorial(n - 1)
end

# ---------------------------------------------------------------------------
# GenServer (stateful process)
# ---------------------------------------------------------------------------
defmodule ZooServer do
  use GenServer

  # Client API
  def start_link(opts \\ []), do: GenServer.start_link(__MODULE__, [], opts)
  def add(pid, organism),     do: GenServer.call(pid, {:add, organism})
  def all(pid),               do: GenServer.call(pid, :all)
  def top(pid, n),            do: GenServer.call(pid, {:top, n})

  # Callbacks
  @impl true
  def init(_), do: {:ok, []}

  @impl true
  def handle_call({:add, org}, _from, state), do: {:reply, :ok, [org | state]}
  def handle_call(:all,        _from, state), do: {:reply, state, state}
  def handle_call({:top, n},   _from, state) do
    top = state |> Enum.sort_by(& &1.intelligence, :desc) |> Enum.take(n)
    {:reply, top, state}
  end
end

# ---------------------------------------------------------------------------
# Pipe operator + Enum
# ---------------------------------------------------------------------------
defmodule Pipeline do
  def run(organisms) do
    organisms
    |> Enum.filter(&(&1.intelligence > 70))
    |> Enum.map(&Describable.describe/1)
    |> Enum.sort()
  end
end

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
organisms = [
  Organism.new("Zorgon",  "Kepler-442b", 95),
  Organism.new("Blorbax", "Gliese 667C", 72),
  Organism.new("Floopix", "Proxima b",   88),
  Organism.new("Grumbix", "HD 40307g",   61),
]

IO.puts("=== All Organisms ===")
Enum.each(organisms, &IO.puts("  #{Describable.describe(&1)}"))

IO.puts("\n=== Fibonacci (0..9) ===")
IO.inspect(Enum.map(0..9, &Math.fibonacci/1))

IO.puts("\n=== GenServer ===")
{:ok, pid} = ZooServer.start_link()
Enum.each(organisms, &ZooServer.add(pid, &1))
top2 = ZooServer.top(pid, 2)
IO.puts("Top 2:")
Enum.each(top2, &IO.puts("  #{Describable.describe(&1)}"))

IO.puts("\n=== Pipeline (IQ > 70) ===")
Pipeline.run(organisms) |> Enum.each(&IO.puts("  #{&1}"))
