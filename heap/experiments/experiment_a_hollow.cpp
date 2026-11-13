// experiment_a_hollow.cpp
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>

#include "graph.h"
#include "dijkstra.h"
#include "hollow_heap.h"

int main(int argc, char** argv) {
    std::vector<std::string> datasetFiles = {
        "Hongkong.road-d",
        "Chongqing.road-d",
        "Shanghai.road-d"
    };

    std::cout << "=== Experiment A — Hollow Heap (Static Routing with Dijkstra) ===\n\n";

    if (argc < 2) {
        std::cerr << "Usage: ./expA_hollow <datasetIndex>\n";
        std::cerr << "Example: ./expA_hollow 0\n";
        return 1;
    }

    int idx = std::stoi(argv[1]);
    if (idx < 0 || idx >= (int)datasetFiles.size()) {
        std::cerr << "Invalid dataset index. Must be 0, 1, or 2.\n";
        return 1;
    }

    Graph g;
    if (!g.loadRoadD(datasetFiles[idx])) {
        std::cerr << "Failed to load dataset: " << datasetFiles[idx] << "\n";
        return 1;
    }

    std::cout << "Using dataset index: " << idx << "\n";
    std::cout << "Dataset: " << datasetFiles[idx] << "\n";
    std::cout << "Loaded graph: " << g.numVertices()
              << " vertices, " << g.numEdges() << " edges\n\n";

    DijkstraMetrics metrics;
    DijkstraResult res = runDijkstra<HollowHeap>(g, 0, metrics);

    // Separate HollowHeap instance just for structural estimates
    HollowHeap heapStats;
    int heapHeight = heapStats.getHeightEstimate();
    int numTrees   = heapStats.getNumTrees();
    long long cascadingCuts = heapStats.getNumCascadingCuts();
    double memMB   = heapStats.getMemoryUsageMBEstimate();

    // Append (do NOT overwrite) the results file
    std::ofstream out("experiment_A_hollow.txt", std::ios::app);
    if (!out.is_open()) {
        std::cerr << "Error: could not open experiment_A_hollow.txt for writing.\n";
        return 1;
    }

    out << "Experiment A - Hollow Heap\n";
    out << "Dataset index: " << idx << "\n";
    out << "Dataset: " << datasetFiles[idx] << "\n";
    out << "Vertices: " << g.numVertices() << "\n";
    out << "Edges: " << g.numEdges() << "\n";
    out << std::fixed << std::setprecision(5);
    out << "Total runtime (ms): " << metrics.runtimeMs << "\n";
    out << "Insert operations: " << metrics.inserts << "\n";
    out << "Extract-min operations: " << metrics.extractMins << "\n";
    out << "Decrease-key operations: " << metrics.decreaseKeys << "\n";
    out << "Heap height estimate: " << heapHeight << "\n";
    out << "Number of trees: " << numTrees << "\n";
    out << "Cascading cuts: " << cascadingCuts << "\n";
    out << "Memory usage estimate (MB): " << memMB << "\n";
    out << "----------------------------------------\n\n";

    out.close();

    std::cout << "Results appended to experiment_A_hollow.txt\n";
    return 0;
}
