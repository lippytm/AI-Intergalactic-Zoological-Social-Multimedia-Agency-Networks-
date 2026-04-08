#!/usr/bin/env bash
# Shell / Bash Starter — Functions, arrays, associative arrays, error handling, subshells
# Run: bash main.sh

set -euo pipefail
IFS=$'\n\t'

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------
RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; RESET='\033[0m'
info()    { echo -e "${CYAN}[INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}[OK]${RESET}    $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*" >&2; }

# ---------------------------------------------------------------------------
# Arrays
# ---------------------------------------------------------------------------
declare -a PLANETS=("Earth" "Kepler-442b" "Proxima b" "Gliese 667Cc")
declare -A PLANET_GALAXY=(
    ["Earth"]="Milky Way"
    ["Kepler-442b"]="Milky Way"
    ["Proxima b"]="Milky Way"
    ["Gliese 667Cc"]="Scorpius"
)

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------
lookup_galaxy() {
    local planet="$1"
    echo "${PLANET_GALAXY[$planet]:-Unknown}"
}

fibonacci() {
    local n="$1" a=0 b=1
    for (( i=0; i<n; i++ )); do
        printf "%d " "$a"
        local tmp=$((a + b)); a=$b; b=$tmp
    done
    echo
}

# Retry with backoff
retry() {
    local attempts="$1"; shift
    local delay=1
    for (( i=0; i<attempts; i++ )); do
        if "$@"; then return 0; fi
        error "Attempt $((i+1))/$attempts failed. Retrying in ${delay}s …"
        sleep "$delay"; delay=$((delay * 2))
    done
    return 1
}

# ---------------------------------------------------------------------------
# Process substitution & subshells
# ---------------------------------------------------------------------------
count_words() {
    wc -w < <(echo "$1")
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
info "=== Planets and Galaxies ==="
for planet in "${PLANETS[@]}"; do
    galaxy=$(lookup_galaxy "$planet")
    success "$planet → $galaxy"
done

info "\n=== Fibonacci (10 terms) ==="
fibonacci 10

info "\n=== Word count ==="
sentence="The intergalactic zoological society welcomes all species"
words=$(count_words "$sentence")
echo "  \"$sentence\""
echo "  Word count: $words"

info "\n=== Parameter expansion ==="
filename="report_2024-03-01.csv"
echo "  Base:      ${filename%.*}"
echo "  Extension: ${filename##*.}"
echo "  Upper:     ${filename^^}"

info "\n=== Done ==="
