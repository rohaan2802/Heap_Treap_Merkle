// dijkstra.h
#ifndef DIJKSTRA_H
#define DIJKSTRA_H

#include <vector>
#include <limits>
#include <stdexcept>
#include <utility>
#include <chrono>
#include "graph.h"
#include "priority_queue.h"

struct DijkstraResult {
    std::vector<double> dist;
    std::vector<int> parent;
};

struct DijkstraMetrics {
    long long inserts = 0;
    long long extractMins = 0;
    long long decreaseKeys = 0;
    double runtimeMs = 0.0;
};

template <typename PQType>
DijkstraResult runDijkstra(const Graph& g, int source, DijkstraMetrics& metrics) {
    int n = g.numVertices();
    if (source < 0 || source >= n) throw std::out_of_range("source vertex is outside the graph");
    metrics = {};
    std::vector<double> dist(n, std::numeric_limits<double>::infinity());
    std::vector<int> parent(n, -1);
    std::vector<PQNodeBase*> handles(n, nullptr);

    PQType pq;

    auto start = std::chrono::steady_clock::now();

    dist[source] = 0.0;
    handles[source] = pq.insert(0.0, source);
    metrics.inserts++;

    while (!pq.empty()) {
        auto [d, u] = pq.extract_min();
        metrics.extractMins++;
        handles[u] = nullptr;

        for (const auto& e : g.neighbors(u)) {
            int v = e.to;
            double w = e.weight;
            double nd = d + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                parent[v] = u;
                if (handles[v] == nullptr) {
                    handles[v] = pq.insert(nd, v);
                    metrics.inserts++;
                } else {
                    pq.decrease_key(handles[v], nd);
                    metrics.decreaseKeys++;
                }
            }
        }
    }

    auto end = std::chrono::steady_clock::now();
    metrics.runtimeMs =
        std::chrono::duration<double, std::milli>(end - start).count();

    return {std::move(dist), std::move(parent)};
}

#endif // DIJKSTRA_H
