// C++ Starter — Templates, Concepts (C++20), Ranges, Coroutines stub, Smart Pointers
// Compile: g++ -std=c++20 -O2 -o main main.cpp

#include <algorithm>
#include <concepts>
#include <coroutine>
#include <format>
#include <iostream>
#include <map>
#include <memory>
#include <numeric>
#include <ranges>
#include <stdexcept>
#include <string>
#include <vector>

// ---------------------------------------------------------------------------
// Concepts
// ---------------------------------------------------------------------------
template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template<Numeric T>
T clamp(T value, T lo, T hi) {
    return std::max(lo, std::min(value, hi));
}

// ---------------------------------------------------------------------------
// Smart pointers + RAII
// ---------------------------------------------------------------------------
struct Organism {
    std::string name;
    std::string planet;
    uint8_t     intelligence{0};

    std::string describe() const {
        return std::format("{} from {} (IQ: {})", name, planet, intelligence);
    }
};

using OrgPtr = std::shared_ptr<Organism>;

class OrganismRegistry {
    std::map<std::string, OrgPtr> data_;
public:
    void add(OrgPtr org) { data_[org->name] = std::move(org); }

    OrgPtr find(const std::string& name) const {
        if (auto it = data_.find(name); it != data_.end()) return it->second;
        return nullptr;
    }

    std::vector<OrgPtr> topByIntelligence(std::size_t n) const {
        std::vector<OrgPtr> v;
        v.reserve(data_.size());
        for (auto& [_, org] : data_) v.push_back(org);
        std::ranges::sort(v, [](auto& a, auto& b){ return a->intelligence > b->intelligence; });
        if (n < v.size()) v.resize(n);
        return v;
    }
};

// ---------------------------------------------------------------------------
// Variadic template
// ---------------------------------------------------------------------------
template<typename... Args>
void log(Args&&... args) {
    (std::cout << ... << args) << '\n';
}

// ---------------------------------------------------------------------------
// Ranges pipeline
// ---------------------------------------------------------------------------
std::vector<int> evenSquares(int n) {
    auto view = std::views::iota(1, n + 1)
              | std::views::filter([](int x){ return x % 2 == 0; })
              | std::views::transform([](int x){ return x * x; });
    return std::vector<int>(view.begin(), view.end());
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
int main() {
    // Concepts + clamp
    log("clamp(150, 0, 100) = ", clamp(150, 0, 100));

    // Registry
    OrganismRegistry reg;
    reg.add(std::make_shared<Organism>("Zorgon",  "Kepler-442b",   95));
    reg.add(std::make_shared<Organism>("Blorbax", "Gliese 667C",   72));
    reg.add(std::make_shared<Organism>("Floopix", "Proxima b",     88));

    if (auto org = reg.find("Zorgon"); org) {
        log("Found: ", org->describe());
    }

    log("\nTop 2 by intelligence:");
    for (auto& org : reg.topByIntelligence(2)) {
        log("  ", org->describe());
    }

    // Ranges
    auto sq = evenSquares(10);
    std::cout << "Even squares ≤10: ";
    for (int x : sq) std::cout << x << ' ';
    std::cout << '\n';

    // Accumulate
    auto sum = std::accumulate(sq.begin(), sq.end(), 0);
    log("Sum: ", sum);

    return 0;
}
