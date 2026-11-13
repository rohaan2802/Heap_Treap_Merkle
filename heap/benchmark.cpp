#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include "binary_heap.h"
#include "dijkstra.h"
#include "fibonacci_heap.h"
#include "hollow_heap.h"

template <typename Heap>
std::vector<double> benchmark(const char* name, const Graph& graph, int source) {
    DijkstraMetrics metrics;
    auto result = runDijkstra<Heap>(graph, source, metrics);
    std::cout << std::left << std::setw(12) << name << std::right
              << std::setw(11) << metrics.inserts << std::setw(11) << metrics.extractMins
              << std::setw(11) << metrics.decreaseKeys << std::setw(12)
              << std::fixed << std::setprecision(3) << metrics.runtimeMs << '\n';
    return std::move(result.dist);
}

bool same_distances(const std::vector<double>& a, const std::vector<double>& b) {
    return std::equal(a.begin(), a.end(), b.begin(), [](double x, double y) {
        return x == y || (std::isfinite(x) && std::isfinite(y) &&
                          std::abs(x-y) <= 1e-10 * std::max({1.0, std::abs(x), std::abs(y)}));
    });
}

int main(int argc, char** argv) {
    if (argc < 2 || argc > 3) {
        std::cerr << "Usage: heap_benchmark GRAPH [SOURCE]\n";
        return 2;
    }
    try {
        Graph graph;
        if (!graph.loadRoadD(argv[1])) return 2;
        std::size_t end = 0;
        int source = argc == 3 ? std::stoi(argv[2], &end) : 0;
        if (argc == 3 && argv[2][end] != '\0') throw std::invalid_argument("invalid source");
        if (source < 0 || source >= graph.numVertices()) throw std::out_of_range("invalid source");
        std::cout << graph.numVertices() << " vertices | " << graph.numEdges()
                  << " roads | source " << source << "\n\n";
        std::cout << "Heap            Inserts   Extracts  Decreases     Time ms\n";
        const auto binary = benchmark<BinaryHeap>("Binary", graph, source);
        const auto fibonacci = benchmark<FibonacciHeap>("Fibonacci", graph, source);
        const auto hollow = benchmark<HollowHeap>("Hollow", graph, source);
        if (!same_distances(binary, fibonacci) || !same_distances(binary, hollow)) {
            std::cerr << "Shortest-path distances disagree.\n";
            return 1;
        }
        std::cout << "\nDistance check: all three heaps agree\n";
        if (binary.size() <= 12) {
            for (std::size_t v = 0; v < binary.size(); ++v)
                std::cout << "  " << source << " -> " << v << " : " << binary[v] << '\n';
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}
