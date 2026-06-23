-- Haskell Starter — Typeclasses, ADTs, Monads, Functors, IO, where/let
-- Run: runghc main.hs  OR  ghc -O2 -o main main.hs && ./main

module Main where

import Control.Monad (forM_, when)
import Data.List     (maximumBy, sortBy)
import Data.Ord      (comparing, Down(..))
import Data.Maybe    (mapMaybe)
import Data.Map.Strict (Map)
import qualified Data.Map.Strict as Map

-- ---------------------------------------------------------------------------
-- ADTs
-- ---------------------------------------------------------------------------
data PlanetType = Rocky | GasGiant | IceGiant | Dwarf deriving (Show, Eq)

data Planet = Planet
  { planetName   :: String
  , massKg       :: Double
  , radiusKm     :: Double
  , moons        :: [String]
  , planetType   :: PlanetType
  } deriving (Show)

-- ---------------------------------------------------------------------------
-- Typeclass
-- ---------------------------------------------------------------------------
class Describe a where
  describe :: a -> String

instance Describe Planet where
  describe p =
    planetName p <> " (" <> show (planetType p) <> ", "
    <> show (length (moons p)) <> " moon(s))"

-- ---------------------------------------------------------------------------
-- Smart constructor (safe)
-- ---------------------------------------------------------------------------
mkPlanet :: String -> Double -> Double -> [String] -> PlanetType -> Maybe Planet
mkPlanet name mass radius ms pt
  | mass   <= 0 = Nothing
  | radius <= 0 = Nothing
  | otherwise   = Just (Planet name mass radius ms pt)

-- ---------------------------------------------------------------------------
-- Pure functions
-- ---------------------------------------------------------------------------
surfaceGravity :: Planet -> Double
surfaceGravity p =
  let g = 6.674e-11
      r = radiusKm p * 1000
  in g * massKg p / r ^ (2 :: Int)

topPlanets :: Int -> [Planet] -> [Planet]
topPlanets n = take n . sortBy (comparing (Down . massKg))

-- ---------------------------------------------------------------------------
-- Functor / Applicative / Monad usage
-- ---------------------------------------------------------------------------
safeDiv :: Double -> Double -> Maybe Double
safeDiv _ 0 = Nothing
safeDiv a b = Just (a / b)

computation :: Double -> Double -> Double -> Maybe Double
computation x y z = do
  a <- safeDiv x y
  b <- safeDiv a z
  return (a + b)

-- ---------------------------------------------------------------------------
-- Main
-- ---------------------------------------------------------------------------
main :: IO ()
main = do
  let planets = mapMaybe id
        [ mkPlanet "Earth"       5.972e24 6_371  ["Moon"]  Rocky
        , mkPlanet "Jupiter"     1.898e27 69_911 []        GasGiant
        , mkPlanet "Neptune"     1.024e26 24_622 ["Triton"] IceGiant
        , mkPlanet "Pluto"       1.303e22 1_188  ["Charon"] Dwarf
        ]

  putStrLn "=== All planets ==="
  forM_ planets $ \p -> do
    putStrLn $ "  " <> describe p
    putStrLn $ "    surface gravity: " <> show (surfaceGravity p) <> " m/s²"

  putStrLn "\n=== Top 2 by mass ==="
  forM_ (topPlanets 2 planets) $ \p ->
    putStrLn $ "  " <> planetName p

  putStrLn "\n=== Monadic computation ==="
  print (computation 100 4 5)   -- Just 30.0
  print (computation 100 0 5)   -- Nothing
