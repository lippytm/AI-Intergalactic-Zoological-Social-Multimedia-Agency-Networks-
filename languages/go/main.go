// Go Starter — Interfaces, Goroutines, Channels, Generics, Error Wrapping
// Run: go run main.go

package main

import (
	"context"
	"errors"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// ---------------------------------------------------------------------------
// Interfaces
// ---------------------------------------------------------------------------

type Describer interface {
	Describe() string
}

// ---------------------------------------------------------------------------
// Generics (Go 1.18+)
// ---------------------------------------------------------------------------

type Set[T comparable] struct {
	items map[T]struct{}
	mu    sync.RWMutex
}

func NewSet[T comparable]() *Set[T] {
	return &Set[T]{items: make(map[T]struct{})}
}

func (s *Set[T]) Add(v T) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.items[v] = struct{}{}
}

func (s *Set[T]) Contains(v T) bool {
	s.mu.RLock()
	defer s.mu.RUnlock()
	_, ok := s.items[v]
	return ok
}

// ---------------------------------------------------------------------------
// Custom error types
// ---------------------------------------------------------------------------

type PlanetError struct {
	Planet string
	Reason string
}

func (e *PlanetError) Error() string {
	return fmt.Sprintf("planet %q: %s", e.Planet, e.Reason)
}

var ErrUnknownPlanet = errors.New("unknown planet")

func lookupPlanet(name string) (string, error) {
	planets := map[string]string{
		"Earth":         "Milky Way",
		"Kepler-442b":   "Cygnus",
		"Proxima b":     "Centaurus",
	}
	if g, ok := planets[name]; ok {
		return g, nil
	}
	return "", fmt.Errorf("%w: %s", ErrUnknownPlanet, name)
}

// ---------------------------------------------------------------------------
// Concurrency — goroutines + channels
// ---------------------------------------------------------------------------

type SensorReading struct {
	Sensor string
	Value  float64
}

func simulateSensor(ctx context.Context, name string, ch chan<- SensorReading, wg *sync.WaitGroup) {
	defer wg.Done()
	for {
		select {
		case <-ctx.Done():
			return
		case <-time.After(100 * time.Millisecond):
			ch <- SensorReading{Sensor: name, Value: rand.Float64() * 100}
		}
	}
}

func collectReadings(duration time.Duration) []SensorReading {
	ctx, cancel := context.WithTimeout(context.Background(), duration)
	defer cancel()

	ch := make(chan SensorReading, 32)
	var wg sync.WaitGroup
	sensors := []string{"temperature", "pressure", "radiation"}

	for _, s := range sensors {
		wg.Add(1)
		go simulateSensor(ctx, s, ch, &wg)
	}

	go func() {
		wg.Wait()
		close(ch)
	}()

	var readings []SensorReading
	for r := range ch {
		readings = append(readings, r)
	}
	return readings
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

func main() {
	// Generics
	s := NewSet[string]()
	s.Add("Zorgon")
	s.Add("Blorbax")
	fmt.Println("Set contains Zorgon:", s.Contains("Zorgon"))
	fmt.Println("Set contains Human:", s.Contains("Human"))

	// Error handling
	for _, planet := range []string{"Earth", "Mars", "Kepler-442b"} {
		galaxy, err := lookupPlanet(planet)
		if err != nil {
			if errors.Is(err, ErrUnknownPlanet) {
				fmt.Printf("⚠ %s\n", err)
			} else {
				fmt.Printf("unexpected error: %s\n", err)
			}
			continue
		}
		fmt.Printf("✓ %s is in galaxy %s\n", planet, galaxy)
	}

	// Concurrency
	fmt.Println("\nCollecting sensor readings for 300ms …")
	readings := collectReadings(300 * time.Millisecond)
	fmt.Printf("Collected %d readings\n", len(readings))
	if len(readings) > 0 {
		r := readings[0]
		fmt.Printf("Sample: sensor=%s value=%.2f\n", r.Sensor, r.Value)
	}
}
