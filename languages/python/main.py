"""
Python Starter — Core Language Features
========================================
Covers: type hints, dataclasses, generators, async/await, decorators, and more.
"""

from __future__ import annotations

import asyncio
import functools
import time
from dataclasses import dataclass, field
from typing import Generator, TypeVar

T = TypeVar("T")

# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass(order=True)
class Planet:
    name: str
    mass_kg: float
    radius_km: float
    moons: list[str] = field(default_factory=list)

    _G: float = 6.674e-11  # gravitational constant m³ kg⁻¹ s⁻²

    @property
    def surface_gravity(self) -> float:
        """Approximate surface gravity (m/s²)."""
        r = self.radius_km * 1_000
        return self._G * self.mass_kg / r ** 2


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def fibonacci() -> Generator[int, None, None]:
    """Infinite Fibonacci generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# ---------------------------------------------------------------------------
# Decorators
# ---------------------------------------------------------------------------

def retry(times: int = 3, delay: float = 0.5):
    """Retry a function up to *times* on exception."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    if attempt == times - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# Async / await
# ---------------------------------------------------------------------------

async def fetch_data(url: str) -> str:
    """Simulate an async HTTP fetch."""
    await asyncio.sleep(0.1)
    return f"<response from {url}>"


async def fetch_many(urls: list[str]) -> list[str]:
    return await asyncio.gather(*[fetch_data(u) for u in urls])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    earth = Planet("Earth", mass_kg=5.972e24, radius_km=6_371, moons=["Moon"])
    print(f"{earth.name}: surface gravity ≈ {earth.surface_gravity:.2f} m/s²")

    # Remove the unused generator assignment
    gen = fibonacci()
    print("First 10 Fibonacci:", [next(gen) for _ in range(10)])

    urls = ["https://example.com", "https://example.org"]
    results = asyncio.run(fetch_many(urls))
    print("Async fetch results:", results)
