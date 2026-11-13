<div align="center">

# Heap, Treap & Merkle

**Algorithms coursework in C++ and Python**

Shortest paths on road networks, score-prioritized feeds, and SHA-256 review integrity.

[![C++: C++17](assets/badges/cpp.svg)](heap/README.md)
[![Python: Feed and proofs](assets/badges/python.svg)](treap/trees.py)
[![Build: CMake](assets/badges/cmake.svg)](CMakeLists.txt)
[![Integrity: SHA-256](assets/badges/sha256.svg)](merkle/merkle.py)
[![Gallery: 24 screenshots](assets/badges/gallery.svg)](#screenshots)
[![Data: GitHub Releases](assets/badges/release.svg)](https://github.com/rohaan2802/Heap_Treap_Merkle/releases)

</div>

---

## Live Links

| What | Link |
| --- | --- |
| Repository | [https://github.com/rohaan2802/Heap_Treap_Merkle](https://github.com/rohaan2802/Heap_Treap_Merkle) |
| Website (GitHub Pages) | [https://rohaan2802.github.io/Heap_Treap_Merkle/](https://rohaan2802.github.io/Heap_Treap_Merkle/) |
| Releases | [https://github.com/rohaan2802/Heap_Treap_Merkle/releases](https://github.com/rohaan2802/Heap_Treap_Merkle/releases) |

The Pages address becomes available after deployment. Full road datasets are packaged for the release.

---

## Table of Contents

1. [Live Links](#live-links)
2. [Overview](#overview)
3. [What's Inside](#whats-inside)
4. [Heap and Shortest Paths](#heap-and-shortest-paths)
5. [Heap File and Experiment Guide](#heap-file-and-experiment-guide)
6. [Treap and BST Feed Study](#treap-and-bst-feed-study)
7. [Feed File and Operation Guide](#feed-file-and-operation-guide)
8. [Merkle Tree and Review Integrity](#merkle-tree-and-review-integrity)
9. [Merkle File and Menu Guide](#merkle-file-and-menu-guide)
10. [Reports and Coursework](#reports-and-coursework)
11. [Coursework and Report Index](#coursework-and-report-index)
12. [Original Submissions](#original-submissions)
13. [Data and Release Downloads](#data-and-release-downloads)
14. [Results and Trade-offs](#results-and-trade-offs)
15. [Folder Structure](#folder-structure)
16. [How to Use This Repository](#how-to-use-this-repository)
17. [How to Compile and Run](#how-to-compile-and-run)
18. [Screenshots](#screenshots)
19. [Credits](#credits)

---

## Overview

The project studies how data structures affect three different jobs: finding routes, ranking posts, and checking records.

- **Shortest paths.** The C++ benchmark runs Dijkstra with three min-priority queues and compares all resulting distances.
- **Ordered feeds.** Two Python trees support the same feed operations. The benchmark shows what changes when a tree also orders nodes by score.
- **Review integrity.** A SHA-256 Merkle tree commits to a sequence of reviews and supports proofs for individual records.

## What's Inside

| Area | Contents | Start here |
| --- | --- | --- |
| Heap study | Graph loader, Dijkstra, three priority queues, and benchmark drivers | [Open](heap/README.md) |
| Feed study | BST and treap implementations, experiment helpers, CLI, and notebook | [Open](treap/reddit-feed-study.ipynb) |
| Review integrity | JSON Lines loader, SHA-256 tree, inclusion proofs, and CLI | [Open](merkle/merkle.py) |
| Data | Small runnable fixtures and the full road archive inventory | [Open](data/README.md) |
| Reports | Original experimental methods and results | [Open](docs/reports/heap-report.pdf) |
| Coursework | Problem statements, rubrics, and four Assignment 03 solutions | [Open](docs/coursework/assignment-03/README.md) |

## Heap and Shortest Paths

Dijkstra reads an undirected weighted edge list. It requires nonnegative weights and uses a priority queue keyed by tentative distance.

- **Binary heap.** An array stores nodes and their positions. Sift operations restore heap order after insertion, extraction, or a decrease.
- **Fibonacci heap.** A forest defers consolidation until extract-min. Cuts and cascading cuts restore order after a decrease.
- **Hollow heap.** Stable item handles follow items to fresh nodes. The queue discards hollow roots during extraction and consolidates the surviving roots.
- **Experiments A and B.** Experiment A runs Dijkstra on road networks. Experiment B exercises priority queues with synthetic operations. The consolidated benchmark reports insertions, extractions, decreases, and elapsed time.
- **Parallel and tracked runs.** The bonus code runs independent sources over one graph and records changes in the Fibonacci heap over the course of Dijkstra.

[Benchmark source](heap/benchmark.cpp) · [Heap experiment guide](heap/README.md) · [Original heap report](docs/reports/heap-report.pdf)

### Heap Inputs, Outputs, and Experiments

- **Graph format.** Use one from–to–weight triple per line. Vertex IDs start at zero, and the highest ID determines the number of vertices. Lines beginning with # are comments. The loader treats each edge as undirected and rejects negative weights.
- **Tracing the sample.** From vertex 0, the route to vertex 1 improves from the direct cost of 8 to a cost of 3 via vertex 2. The final distances to vertices 0 through 4 are 0, 3, 2, 5, and 8. Vertices 5 and 6 are unreachable from 0.
- **Reading the benchmark.** Inserts count the first discovery of each vertex. Decreases count improvements to a vertex already queued. Extracts count removals of the current minimum. The benchmark compares distances, since equal-cost routes can have different predecessors.
- **Optional coursework runs.** Experiment A applies Dijkstra to a road graph. Experiment B profiles synthetic insert, extract-min, and decrease-key operations. The parallel run assigns independent source vertices to workers over a shared graph. The evolution run exports CSV counters for the Fibonacci heap plotting script.
- **Road data and filenames.** The release package contains Hongkong.road-d, Chongqing.road-d, Shanghai.road-d, and ShanghaiNew.road-D. Use the exact filename on systems that distinguish uppercase and lowercase letters.

[Heap experiment guide](heap/README.md) · [Graph loader](heap/include/graph.h) · [Dijkstra source](heap/include/dijkstra.h)

## Heap File and Experiment Guide

| File or target | Role | Open |
| --- | --- | --- |
| benchmark.cpp | Runs all three queues on the same graph and compares their distance arrays | [Open](heap/benchmark.cpp) |
| priority_queue.h | Shared operations and node handle interface | [Open](heap/include/priority_queue.h) |
| graph.h / dijkstra.h | Loads the road edge list and computes distances and predecessors | [Open](heap/include/dijkstra.h) |
| binary_heap.h | Array-backed queue with index tracking and sift operations | [Open](heap/include/binary_heap.h) |
| fibonacci_heap.h | Root consolidation, decrease-key cuts, and cascading cuts | [Open](heap/include/fibonacci_heap.h) |
| hollow_heap.h | Stable item handles and cleanup of hollow roots during extract-min | [Open](heap/include/hollow_heap.h) |
| Experiment A | Separate routing drivers for Binary, Fibonacci, and Hollow heaps | [Open](heap/experiments/experiment_a_binary.cpp) |
| Experiment B | Separate operation profiling drivers for the same three queues | [Open](heap/experiments/experiment_b_binary.cpp) |
| Parallel benchmark | Runs independent shortest-path searches over one read-only graph | [Open](heap/bonus/parallel_benchmark.cpp) |
| Heap evolution | Records heap size, estimated height, tree count, and cuts to CSV | [Open](heap/bonus/heap_evolution.cpp) |
| Evolution plots | Plots the recorded height, tree count, and cascading cuts | [Open](heap/bonus/plot_evolution.py) |

## Treap and BST Feed Study

Both trees order posts by timestamp and post ID. The treap also keeps higher scores above lower scores, so its root holds a most-popular post.

- **Feed operations.** Both implementations support adding and replacing posts, likes, deletion, popularity lookup, and recent posts. An ID map helps find a post for updates.
- **Ordered workload.** Chronological insertion can make a plain BST a chain. A treap rotates when a child outranks its parent. The resulting height depends on how scores relate to timestamps.
- **Benchmark metrics.** The study measures height, rotations, average insertion and deletion time, and the time to query the most popular post. The notebook also shows tree shapes and feed operations.
- **Input data.** The command-line demo and notebook run on synthetic data. A compatible Reddit submission dump can be streamed from compressed JSON Lines for a separate run.

[Feed implementations](treap/trees.py) · [Benchmark implementation](treap/experiments.py) · [Reddit study notebook](treap/reddit-feed-study.ipynb) · [Original treap report](docs/reports/treap-vs-bst-report.pdf)

### Feed Operations and Benchmark Method

- **Post identity and ordering.** Each post has an ID, timestamp, and score. Both trees use the timestamp and ID together as the ordering key. Adding an existing ID replaces the previous entry.
- **Likes and deletion.** The ID map locates the entry to update or remove. The BST can increment a score in place. The treap reinserts the liked post at the new priority so the score ordering stays valid.
- **Popularity and recency.** The BST scans for the highest score. The treap returns its root. Both trees find recent posts by visiting nodes in reverse timestamp and ID order.
- **What is timed.** The benchmark measures adding posts, looking up the most popular post, and deleting posts. It reports average operation times and measures tree height before deletion. The notebook adds tree shapes, rotations, likes, and recent-post examples.
- **Reproducing the workload.** The default CLI generates 1,000 chronological posts from a fixed score sequence. Use --posts to change the size or --dataset to supply a compatible compressed Reddit dump. The synthetic results depend on how timestamps and scores are distributed.

[Feed source](treap/trees.py) · [Benchmark source](treap/experiments.py) · [Study notebook](treap/reddit-feed-study.ipynb)

## Feed File and Operation Guide

| File or operation | Role | Open |
| --- | --- | --- |
| trees.py | Contains BSTFeed, TreapFeed, rotations, traversal, and validators | [Open](treap/trees.py) |
| experiments.py | Runs common workloads and records height, rotations, and operation timings | [Open](treap/experiments.py) |
| dataset_utils.py | Streams compressed Reddit submissions as ID, timestamp, and score tuples | [Open](treap/dataset_utils.py) |
| python -m treap | Runs the synthetic benchmark or reads the optional Reddit input | [Open](treap/__main__.py) |
| Notebook | Runs the study and visualizes height, timings, rotations, and tree shape | [Open](treap/reddit-feed-study.ipynb) |
| addPost / deletePost | Insert or remove by ID. Reusing an ID replaces its previous entry | [Open](treap/trees.py) |
| likePost | Updates the score. The treap restores the heap order by reinserting the post | [Open](treap/trees.py) |
| getMostPopular / getMostRecent | Queries the highest score or returns posts in reverse chronological key order | [Open](treap/trees.py) |

## Merkle Tree and Review Integrity

The loader reads JSON Lines and selects review ID, product ID, rating, and review text. The tree commits to those fields in input order.

- **Tree construction.** Each record becomes a leaf digest. Parent hashes combine child digests, and an unpaired child is repeated for that level. The final root also commits to the leaf count.
- **Inclusion proofs.** The proof carries the sibling hash and side at each level. Verification recomputes the root from the candidate leaf and proof, then compares it with a trusted digest.
- **Tamper detection.** The sample verifies an original review and rejects a changed leaf. The interactive menu can also save a trusted root for the session and demonstrate an edit after reloading a changed copy.
- **Scope of the check.** Verification covers the chosen fields, ordering and record count. It depends on getting the expected root from a trusted source.

[Tree and interactive CLI](merkle/merkle.py) · [Sample reviews](data/sample-reviews.jsonl) · [Original Merkle report](docs/reports/merkle-tree-report.pdf)

### Review Fields, Proofs, and Tampering

- **JSON Lines input.** Each line contains one review object. The loader reads review_id or reviewerID, asin, overall, and reviewText. When the ID is absent it creates one from the record position.
- **Hash construction.** A leaf hashes the four selected fields as an ordered JSON array. Leaf, parent, and root hashes use separate prefixes. The tree repeats the final child at odd levels, and the root commits to the number of leaves.
- **Proof contents.** Each proof step supplies a sibling digest and its side. The verifier uses that side to combine hashes in the correct order, then checks the resulting digest against the trusted root and record count.
- **Interactive workflow.** Load and preview the reviews, build the tree, and save the root for the session. Then verify the current tree, request a proof by review ID, or run the edit simulation. The simulation writes a separate changed copy and rebuilds the tree after reading it back.
- **Scope and scaling.** Changing a covered field, the input order, or the record count changes the commitment. Fields outside the selected four are outside the check. The scaling menu measures tree construction on available record prefixes.

[Merkle implementation](merkle/merkle.py) · [Example reviews](data/sample-reviews.jsonl) · [Original report](docs/reports/merkle-tree-report.pdf)

## Merkle File and Menu Guide

| File or menu step | Role | Open |
| --- | --- | --- |
| ReviewDataset | Reads selected review fields and indexes reviews by ID | [Open](merkle/merkle.py) |
| MerkleTree | Builds SHA-256 levels, produces a sibling path, and verifies an inclusion proof | [Open](merkle/merkle.py) |
| python -m merkle FILE | Runs the proof and tampering demonstration on a chosen JSON Lines file | [Open](merkle/__main__.py) |
| Menu 1–3 | Load a file, preview records, and build the tree | [Open](merkle/merkle.py) |
| Menu 4–6 | Save the root for the session, compare roots, or verify a selected review | [Open](merkle/merkle.py) |
| Menu 7–9 | Simulate an edit, benchmark available prefixes, or exit | [Open](merkle/merkle.py) |
| Sample reviews | Three records for verifying an odd-sized tree and testing a changed leaf | [Open](data/sample-reviews.jsonl) |

## Reports and Coursework

The reports preserve the original experimental setups and measurements. Use the current demos to reproduce the behavior in this repository.

- **Assignment 03.** The original statement and four standalone C++ solutions are organized by question.
- **Project briefs and rubrics.** The heap and treap briefs, all three rubrics, and the evaluation summary document the coursework requirements.

[Assignment 03](docs/coursework/assignment-03/README.md) · [Heap brief](docs/coursework/project-algorithm-heaps.pdf) · [Treap brief](docs/coursework/project-algorithm-treaps.pdf) · [Heap rubric](docs/coursework/rubric-heap-part.pdf) · [Treap rubric](docs/coursework/rubric-treap-part.pdf) · [Merkle rubric](docs/coursework/rubric-merkle-trees-part.pdf) · [Evaluation summary](docs/coursework/rubric-evaluation-summary.pdf)

## Coursework and Report Index

| Resource | Contents | Open |
| --- | --- | --- |
| Heap brief and rubric | Routing and priority-queue requirements | [Open](docs/coursework/project-algorithm-heaps.pdf) |
| Treap brief and rubric | Feed operations and comparison requirements | [Open](docs/coursework/project-algorithm-treaps.pdf) |
| Merkle rubric | Tree construction, proofs, performance, and tamper detection | [Open](docs/coursework/rubric-merkle-trees-part.pdf) |
| Evaluation summary | Combined coursework evaluation | [Open](docs/coursework/rubric-evaluation-summary.pdf) |
| Heap report | Implementation design, original measurements, and analysis | [Open](docs/reports/heap-report.pdf) |
| Feed report | Dataset, workload, results, and original figures | [Open](docs/reports/treap-vs-bst-report.pdf) |
| Merkle report | Original SHA-256 integrity workflow and scaling measurements | [Open](docs/reports/merkle-tree-report.pdf) |
| Assignment 03 | Statement and standalone C++ solutions organized by question | [Open](docs/coursework/assignment-03/README.md) |

## Original Submissions

Original notebook and report revisions are indexed in [Original submissions](docs/original-submissions/README.md). The original heap text results are in [Heap measurements](docs/reports/heap-results/README.md). Run the original Merkle checks against the current implementation with `python -m unittest merkle.test_merkle`.

## Data and Release Downloads

The bundled graph and reviews let you run the demos immediately. Full road-network inputs belong in the separate release ZIP.

- **Sample graph.** Each row lists two vertex IDs and an edge weight. Two vertices are disconnected from the default source, so the demo also shows unreachable distances.
- **Road networks.** The release ZIP contains Hongkong, Chongqing, Shanghai, and ShanghaiNew. Extract the files into data/ and pass the desired path to the benchmark.
- **Reddit inputs.** Use a compatible .zst submission archive with id, created_utc, and score. Install the notebook dependencies before using the compressed data.

The release asset is **road-network-datasets.zip**. Extract its four road graphs into `data/`.

[Data guide](data/README.md) · [Sample road graph](data/sample.road-d) · [Notebook dependencies](treap/requirements.txt) · [GitHub Releases](https://github.com/rohaan2802/Heap_Treap_Merkle/releases)

## Results and Trade-offs

| Study | What to look for | How to read it |
| --- | --- | --- |
| Heap | All three queues agree on distances for the sample and the 43,620-vertex Hong Kong graph. | The benchmark measures each queue on the same graph. Timings depend on input, build settings, and hardware. |
| Treap | At 1,000 synthetic posts the BST has height 999 and the treap has height 22. | This result comes from chronological inserts and the demo's fixed score sequence. Correlated scores can still produce a deep treap. |
| Merkle | A proof for the original review passes. Changing the leaf fails verification and editing a review changes the root. | Building the tree takes linear time in the number of records. A single inclusion proof uses logarithmically many sibling hashes. |

## Folder Structure

~~~text
Heap_Treap_Merkle/
├── heap/
│   ├── include/          Priority queues, graph loader, Dijkstra
│   ├── experiments/      Standalone coursework experiments
│   └── bonus/            Parallel and tracked experiments
├── treap/                Feed trees, benchmark, notebook
├── merkle/               Review loader, Merkle tree, proofs, CLI
├── data/                 Sample graph and reviews
├── docs/                 Reports, briefs, rubrics, Assignment 03
├── assets/               Website styles, scripts, screenshots
├── CMakeLists.txt        C++ build
├── index.html            Project website
└── README.md
~~~

## How to Use This Repository

1. Start with the sample graph and reviews. The quick start runs all three studies without downloading a dataset.
2. Inspect the file guide for the study you want to reproduce. The benchmark entry points and original experiment drivers are listed separately.
3. Read the report alongside the current demo. The reports preserve the original workloads and measurements, while the gallery identifies current runs and original figures.
4. Use the release archive for full road-network experiments, or supply a compatible Reddit dump for the notebook. The data guide describes both inputs.

## How to Compile and Run

### Quick Start

Run from the repository root. The Python sample demos use the standard library. For C++, use CMake and a C++17 compiler.

~~~sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
./build/heap_benchmark data/sample.road-d
python -m treap
python -m merkle data/sample-reviews.jsonl
~~~

### More Ways to Run

The first command starts Dijkstra at vertex 2. The second opens the interactive Merkle menu. The last two prepare the optional Reddit workload.

~~~sh
./build/heap_benchmark data/sample.road-d 2
python -m merkle
python -m pip install -r treap/requirements.txt
python -m treap --dataset data/RC_2019-04.zst --posts 10000
~~~

With Visual Studio, run ./build/Release/heap_benchmark.exe. With MinGW, use -G "MinGW Makefiles" at configure time if needed. Set -DBUILD_COURSEWORK_EXPERIMENTS=ON to build the standalone heap experiments.

## Screenshots

24 captures of the source, demos, study figures, and reports. Select any image to open its full 1440 × 900 version.

### Dijkstra on the sample road graph

[![Dijkstra on the sample road graph](assets/screenshots/01-heap-shortest-paths.png)](assets/screenshots/01-heap-shortest-paths.png)

All three queues agree on the distances from vertex 0. Vertices 5 and 6 are unreachable.

### Binary heap insertion

[![Binary heap insertion](assets/screenshots/02-binary-heap.png)](assets/screenshots/02-binary-heap.png)

Insertion appends a node to the array, then restores heap order by sifting up.

### Fibonacci heap extraction

[![Fibonacci heap extraction](assets/screenshots/03-fibonacci-heap.png)](assets/screenshots/03-fibonacci-heap.png)

Extract-min promotes children of the minimum and prepares the roots for consolidation.

### Hollow heap decrease-key

[![Hollow heap decrease-key](assets/screenshots/04-hollow-heap.png)](assets/screenshots/04-hollow-heap.png)

A stable item handle moves to a new node while the old node becomes hollow.

### Edge relaxation

[![Edge relaxation](assets/screenshots/05-dijkstra-relaxation.png)](assets/screenshots/05-dijkstra-relaxation.png)

Dijkstra inserts newly discovered vertices and decreases the key when it finds a better route.

### Hong Kong road network

[![Hong Kong road network](assets/screenshots/06-hongkong-road-network.png)](assets/screenshots/06-hongkong-road-network.png)

The full Hong Kong graph exercises all three queues. The distances agree across 43,620 vertices.

### Parallel Dijkstra benchmark

[![Parallel Dijkstra benchmark](assets/screenshots/07-parallel-dijkstra.png)](assets/screenshots/07-parallel-dijkstra.png)

Independent source runs share the graph. The report compares one worker with four workers.

### Treap vs. BST benchmark

[![Treap vs. BST benchmark](assets/screenshots/08-treap-feed-benchmark.png)](assets/screenshots/08-treap-feed-benchmark.png)

The synthetic chronological workload shows how a plain BST can become a chain. Timings are from one local run.

### Tree height by feed size

[![Tree height by feed size](assets/screenshots/09-tree-height.png)](assets/screenshots/09-tree-height.png)

The original study plots BST and treap height as the number of posts grows.

### Height relative to log₂(n)

[![Height relative to log₂(n)](assets/screenshots/10-height-ratio.png)](assets/screenshots/10-height-ratio.png)

The original study compares height divided by log₂(n) across sample sizes.

### Insertion time by feed size

[![Insertion time by feed size](assets/screenshots/11-insertion-time.png)](assets/screenshots/11-insertion-time.png)

The original study measures average insertion time as the feed grows.

### Most popular post lookup

[![Most popular post lookup](assets/screenshots/12-popularity-lookup.png)](assets/screenshots/12-popularity-lookup.png)

The original study compares a BST scan with access to the treap root.

### Deletion time by feed size

[![Deletion time by feed size](assets/screenshots/13-deletion-time.png)](assets/screenshots/13-deletion-time.png)

The original study measures the average time to remove a post.

### Rotations during treap insertion

[![Rotations during treap insertion](assets/screenshots/14-treap-rotations.png)](assets/screenshots/14-treap-rotations.png)

The original study counts rotations as more posts are inserted.

### Shape of the binary search tree

[![Shape of the binary search tree](assets/screenshots/15-bst-shape.png)](assets/screenshots/15-bst-shape.png)

The example’s timestamp order produces a right-leaning BST.

### Shape of the score-prioritized treap

[![Shape of the score-prioritized treap](assets/screenshots/16-treap-shape.png)](assets/screenshots/16-treap-shape.png)

The same example posts form a different shape when score determines priority.

### Verify a review against the root

[![Verify a review against the root](assets/screenshots/17-merkle-inclusion-proof.png)](assets/screenshots/17-merkle-inclusion-proof.png)

The original review proof passes. A changed leaf fails against the same trusted root.

### Build the Merkle tree

[![Build the Merkle tree](assets/screenshots/18-merkle-tree-build.png)](assets/screenshots/18-merkle-tree-build.png)

The build hashes the selected review fields, then combines pairs of child digests from the bottom up.

### Follow the proof path

[![Follow the proof path](assets/screenshots/19-merkle-proof-path.png)](assets/screenshots/19-merkle-proof-path.png)

The proof keeps a sibling hash and its direction for each level on the path to the root.

### Detect an edited review

[![Detect an edited review](assets/screenshots/20-merkle-tamper-check.png)](assets/screenshots/20-merkle-tamper-check.png)

The interactive demo saves a changed copy, reloads it, and compares its root with the saved digest.

### Merkle scaling results

[![Merkle scaling results](assets/screenshots/21-merkle-scaling-report.png)](assets/screenshots/21-merkle-scaling-report.png)

The original report records build time and memory at several dataset sizes. These are historical measurements.

### Heap implementation report

[![Heap implementation report](assets/screenshots/22-heap-design-report.png)](assets/screenshots/22-heap-design-report.png)

The original heap report explains how the three queue implementations were built.

### Treap experiment setup

[![Treap experiment setup](assets/screenshots/23-treap-study-report.png)](assets/screenshots/23-treap-study-report.png)

The original report describes the feed structures, dataset setup, and measurement method.

### Assignment 03 statement

[![Assignment 03 statement](assets/screenshots/24-assignment-03.png)](assets/screenshots/24-assignment-03.png)

The original assignment brief accompanies four independent C++ solutions.

## Credits

Algorithms coursework by Mohammad Rohaan, Ali Bin Salman, and Muhammad Danish. The individual reports identify the contributors for each study.

[GitHub profile](https://github.com/rohaan2802)
