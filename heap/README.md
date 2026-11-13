# Heap experiments

`heap_benchmark` runs the same graph and source through each queue, reports operation counts, and compares the final distances. The graph loader treats each input edge as undirected.

Set `BUILD_COURSEWORK_EXPERIMENTS=ON` in CMake to build the original Experiment A and B drivers, plus the parallel and heap evolution examples. Run the original drivers in a directory containing the road data. They can write result files to their current working directory. The consolidated benchmark prints results directly to the terminal.

The hollow queue uses stable item handles and lazily removes hollow nodes when they reach the root list. Its decrease operation moves the item to a fresh root; the benchmark does not assume the optimal amortized bound of the ranked two-parent variant.
