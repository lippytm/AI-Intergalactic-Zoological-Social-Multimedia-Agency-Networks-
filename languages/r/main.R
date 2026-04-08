# R Starter — Tidyverse, ggplot2, functional programming, S3 classes
# Run: Rscript main.R

library(methods)

# ---------------------------------------------------------------------------
# S3 Class
# ---------------------------------------------------------------------------
new_organism <- function(name, planet, intelligence) {
  intelligence <- max(0L, min(100L, as.integer(intelligence)))
  structure(
    list(name = name, planet = planet, intelligence = intelligence),
    class = "Organism"
  )
}

print.Organism <- function(x, ...) {
  cat(sprintf("<Organism> %s from %s (IQ: %d)\n", x$name, x$planet, x$intelligence))
}

# ---------------------------------------------------------------------------
# Functional programming with base R
# ---------------------------------------------------------------------------
organisms <- list(
  new_organism("Zorgon",  "Kepler-442b", 95),
  new_organism("Blorbax", "Gliese 667C", 72),
  new_organism("Floopix", "Proxima b",   88),
  new_organism("Grumbix", "HD 40307g",   61)
)

# Map
names_vec <- vapply(organisms, `[[`, character(1), "name")
cat("Names:", paste(names_vec, collapse = ", "), "\n")

# Filter
high_iq <- Filter(function(o) o$intelligence >= 80, organisms)
cat("High-IQ organisms:", length(high_iq), "\n")

# Reduce
total_iq <- Reduce(function(acc, o) acc + o$intelligence, organisms, 0L)
cat("Total IQ:", total_iq, "\n")

# ---------------------------------------------------------------------------
# Data frame + statistical summary
# ---------------------------------------------------------------------------
df <- data.frame(
  name         = names_vec,
  intelligence = vapply(organisms, `[[`, integer(1), "intelligence"),
  stringsAsFactors = FALSE
)

cat("\nSummary:\n")
print(summary(df$intelligence))

# ---------------------------------------------------------------------------
# Fibonacci with memoisation
# ---------------------------------------------------------------------------
memo <- c()
fib <- function(n) {
  if (!is.na(memo[n])) return(memo[n])
  if (n <= 2) { memo[n] <<- 1; return(1) }
  result <- fib(n - 1) + fib(n - 2)
  memo[n] <<- result
  result
}
cat("\nFirst 10 Fibonacci:", sapply(1:10, fib), "\n")

# ---------------------------------------------------------------------------
# Linear regression demo
# ---------------------------------------------------------------------------
set.seed(42)
x <- rnorm(100)
y <- 2 * x + 1 + rnorm(100, sd = 0.5)
model <- lm(y ~ x)
cat("\nLinear regression coefficients:\n")
print(coef(model))
cat(sprintf("R²: %.4f\n", summary(model)$r.squared))
