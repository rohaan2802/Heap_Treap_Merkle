# Heap, Treap, and Merkle Tree — Algorithms Project

Algorithms course package covering **binary heaps**, **treaps vs BSTs** on Reddit-feed-style workloads, and **Merkle trees**: problem statements, three rubrics, Treap-vs-BST report + Jupyter notebooks, heap team zip, Kaggle upload stub (`dataset-metadata.json`, `sda.txt`), and figure exports.

**Author:** Mohammad Rohaan · **Roll:** 22I-2327 · **GitHub:** [rohaan2802](https://github.com/rohaan2802) · **Collaborators (heap zip):** 22i-0894, 22i-1305 · **Section D/B materials** in archived zips

---

## Table of contents

1. [Problem and context](#problem-and-context)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Algorithms](#algorithms)
5. [File-by-file reference](#file-by-file-reference)
6. [I/O formats](#io-formats)
7. [Tech stack](#tech-stack)
8. [Repository structure](#repository-structure)
9. [Build and run](#build-and-run)
10. [Usage](#usage)
11. [Constants](#constants)
12. [Results](#results)
13. [Limitations](#limitations)
14. [How to extend](#how-to-extend)
15. [Author](#author)

---

## Problem and context

The course split the project into three graded parts (see `TREE.txt`):

| Part | Rubric / statement (GitHub) | Intent |
|------|------------------------------|--------|
| **Heap** | `Rubric - Heap Part.pdf`, `Project Statement - Heap Part.zip` | Priority queue: insert, extract-min/max, heapify, decrease-key; array layout |
| **Treap** | `Rubric - Treap Part.pdf`, `Project Algorithm - Treaps.pdf` | Randomized BST: heap property on random priorities + BST on keys; compare to unbalanced BST on feed data |
| **Merkle tree** | `Rubric - Merkle Trees Part.pdf` | Hash tree: leaf hashes, parent `H(left‖right)`, inclusion proofs |

Experimental narrative (notebooks + `Treap_vs_BST_Report`): a **Reddit-like feed** — chronological inserts, lookups by id, and mixed updates — stresses **unbalanced BSTs** (sorted insert → degenerate chain) while a **treap** stays expected O(log n) via random heap priorities.

This working copy extracted only `sda.txt` and `dataset-metadata.json` (Kaggle helper). Notebooks and PDFs remain on GitHub under `ALGO_PROJECT/`.

---

## Features

- Side-by-side **treap vs BST** report (`Treap_vs_BST_Report.pdf` / `.docx`) and two notebooks (`treap-vs-bst-reddit-feed.ipynb`, `-updated.ipynb`).
- Algorithm notes PDF for treaps.
- Heap submission zip shared with 22i-0894 and 22i-1305.
- Merkle rubric + `Rubric evaluation summary.pdf`.
- Extra problems: `Problem1.docx`, `Problem2.docx`, `Problem 3.pdf`.
- Plot exports `download1.png` … `download8.png`, `Capture.PNG`.
- Kaggle dataset stub titled **“My Archive Dataset”**, id `mrohaan28/archive-dataset`, license **CC0-1.0**.
- Section archives: `22i_2327_A3_Sec_D.zip`, `22I-2327_D.zip`, `22i-1305_B.zip`.

---

## Architecture

```
                    ┌─────────────┐
                    │  Heap part  │  array heap / d-ary / pairing (see zip)
                    └─────────────┘
                    ┌─────────────┐
  Reddit-like keys ─►│    BST     │── times, rotations=0, height ~ n
                    │   Treap    │── random priority, rotations, height ~ log n
                    └─────────────┘
                    ┌─────────────┐
  File chunks/tx   ─►│ Merkle tree│── root hash, audit path
                    └─────────────┘

kaggle_upload/
  dataset-metadata.json  +  sda.txt (CLI recipe)
```

**Treap node (canonical):** `key`, `priority` (random), `left`, `right`. BST order on `key`; max-heap (or min-heap) on `priority`. Split/merge implement insert/delete without a parent pointer.

**Merkle node:** leaf `H(data)`; internal `H(H_left ‖ H_right)`; proof = sibling hashes on the path to root.

---

## Algorithms

### Binary heap (array)

Index `i`: parent `(i-1)//2`, children `2i+1`, `2i+2` (0-based). `sift_up` after insert; `sift_down` after extract. Build-heap: sift-down from last parent — O(n). Used for Dijkstra, Huffman, event queues. Exact API is in `Project Statement - Heap Part.zip` / the team zip sources.

### Treap vs BST (feed workload)

**BST insert:** standard walk; sorted keys (monotonic post ids / timestamps) produce a **linked list** — O(n) insert/search.

**Treap insert:**

1. BST-insert by key.
2. If heap property violated with parent, **rotate** (left/right) until priorities are heap-ordered.
3. Equivalently: `split(T, key)` → `merge(merge(L, node), R)`.

**Expected height** O(log n) because priorities are random, equivalent to a random BST.

**Reddit-feed experiment (as implied by notebook names):**

- Insert posts in time order (adversarial for BST).
- Measure wall time, comparisons, tree height, rotation counts.
- Query by id / range (feed window).
- Updated notebook likely refreshes plots (`download*.png`).

### Merkle tree

1. Pad to power of two if required by the rubric.
2. Hash leaves (SHA-256 typical in coursework).
3. Build levels upward.
4. **Inclusion proof:** for leaf index i, emit sibling at each level; verifier recomputes root.
5. Tamper: changing one leaf changes O(log n) nodes, not the whole file (contrast with a single file hash).

---

## File-by-file reference

### This working copy

| File | Contents |
|------|----------|
| `dataset-metadata.json` | Kaggle metadata: title `My Archive Dataset`, id `mrohaan28/archive-dataset`, license name `CC0-1.0` |
| `sda.txt` | Windows cmd: set `KAGGLE_API_TOKEN`, `kaggle datasets list`, `cd /d "D:\kaggle_upload"`, `kaggle datasets create -p .` |

### GitHub `ALGO_PROJECT/` (`TREE.txt`)

| Path | Role |
|------|------|
| `treap-vs-bst-reddit-feed.ipynb` | Original experiment notebook |
| `treap-vs-bst-reddit-feed-updated.ipynb` | Revised plots/metrics |
| `Treap_vs_BST_Report.pdf` / `.docx` | Written analysis |
| `Project Algorithm - Treaps.pdf` | Treap algorithm write-up |
| `Project Statement - Heap Part.zip` | Heap spec |
| `Rubric - Heap Part.pdf` | Heap grading |
| `Rubric - Treap Part.pdf` | Treap grading |
| `Rubric - Merkle Trees Part.pdf` | Merkle grading |
| `Rubric evaluation summary.pdf` | Combined scores notes |
| `Problem1.docx`, `Problem2.docx`, `Problem 3.pdf` | Extra problem sets |
| `22i-0894_22i-2327_22i-1305_HEAP.zip` | Team heap code |
| `kaggle_upload/dataset-metadata.json`, `sda.txt` | Publish helper |
| `download1.png`–`download8.png`, `Capture.PNG` | Figures |
| `22I-2327_D.zip`, `22i-1305_B.zip` | Section archives |
| Root `22i_2327_A3_Sec_D.zip` | Section D assignment 3 |

---

## I/O formats

### `dataset-metadata.json`

```json
{
  "title": "My Archive Dataset",
  "id": "mrohaan28/archive-dataset",
  "licenses": [ { "name": "CC0-1.0" } ]
}
```

Kaggle requires this file in the folder passed to `kaggle datasets create -p .` along with the data files to upload (not included here).

### `sda.txt` (commands)

```bat
set KAGGLE_API_TOKEN=KGAT_your_real_token_here
kaggle datasets list
cd /d "D:\kaggle_upload"
kaggle datasets create -p .
```

Replace the placeholder token. Newer Kaggle CLI uses `~/.kaggle/kaggle.json` (`username` + `key`) rather than `KAGGLE_API_TOKEN`; follow current Kaggle docs if `set` does nothing.

### Notebook I/O (expected)

- Input: Reddit dump / synthetic feed CSV (timestamp, post id, score) — exact filename is inside the `.ipynb` on GitHub.
- Output: matplotlib figures saved as `download*.png`; timing tables in the report.

### Merkle proof (typical text format)

```
leaf_index: 5
siblings: <hex>, <hex>, ...
root: <hex>
```

---

## Tech stack

Python 3, Jupyter, NumPy/pandas/matplotlib (notebooks), C/C++ or Java inside the heap zip (extract to confirm), hash library (`hashlib.sha256` in Python Merkle demos), Kaggle CLI, Word/PDF for reports.

---

## Repository structure

```
Heap_Treap_Merkle/
├── 22i_2327_A3_Sec_D.zip
├── dataset-metadata.json      # copy of kaggle_upload/
├── sda.txt
└── ALGO_PROJECT/
    ├── treap-vs-bst-reddit-feed.ipynb
    ├── treap-vs-bst-reddit-feed-updated.ipynb
    ├── Treap_vs_BST_Report.pdf
    ├── Project Algorithm - Treaps.pdf
    ├── Project Statement - Heap Part.zip
    ├── Rubric - *.pdf
    ├── 22i-0894_22i-2327_22i-1305_HEAP.zip
    ├── kaggle_upload/{dataset-metadata.json, sda.txt}
    └── download1.png … download8.png
```

---

## Build and run

### Notebooks

```bash
cd ALGO_PROJECT
python -m venv .venv
.venv\Scripts\activate
pip install jupyter matplotlib numpy pandas
jupyter notebook treap-vs-bst-reddit-feed-updated.ipynb
```

### Heap / Merkle sources

Unzip `22i-0894_22i-2327_22i-1305_HEAP.zip` and `Project Statement - Heap Part.zip`. Compile as documented inside (often `g++ -O2`). Merkle part may be in the same zip or in `22I-2327_D.zip`.

### Kaggle (optional)

1. Create an API token at kaggle.com → put `kaggle.json` in `%USERPROFILE%\.kaggle\`.
2. Copy data files into `kaggle_upload/` next to `dataset-metadata.json`.
3. `kaggle datasets create -p kaggle_upload` (or `version` if the dataset already exists).

**Do not** commit a real `KGAT_…` token. The string in `sda.txt` is a placeholder.

---

## Usage

1. Read the relevant **rubric PDF** before changing code.
2. Run the **updated** treap notebook for the latest charts; cross-check `download*.png` with the report.
3. Heap: implement the statement’s required operations and complexity proofs.
4. Merkle: demonstrate a proof of membership and a failed proof after tampering a leaf.

---

## Constants

| Item | Value |
|------|--------|
| Kaggle dataset id | `mrohaan28/archive-dataset` |
| License | CC0-1.0 |
| Title | My Archive Dataset |
| Heap team rolls | 22i-0894, 22i-2327, 22i-1305 |
| Typical treap priority | 32-bit random int / `random.random()` |
| Typical Merkle hash | SHA-256 (confirm in notebook) |

---

## Results

Quantitative BST vs treap heights/timings are in `Treap_vs_BST_Report.pdf` and the notebooks (GitHub). `download1.png`–`download8.png` are the exported figures. Heap/Merkle numeric results are inside the zips and evaluation summary PDF.

---

## Limitations

- This extract **does not include the notebooks or heap source** — only Kaggle metadata and TREE.
- `sda.txt` uses a dummy API token and a hard-coded `D:\kaggle_upload` path.
- Dataset title “My Archive Dataset” is a stub, not a documented Reddit dump.
- Unbalanced BST vs treap is a **known** result; the value is the feed-shaped workload and plots.
- Merkle trees in coursework often skip second-preimage discussion and salted leaves.

---

## How to extend

- Add a Merkle inclusion-proof notebook beside the treap experiment.
- Parameterize treap priority distributions (geometric vs uniform).
- Benchmark against `std::set` / `sortedcontainers` as extra baselines.
- Upload a real anonymized feed sample under CC0 if the metadata is meant to ship data.

---

## Author

**Mohammad Rohaan**  
Student ID: **22I-2327**  
GitHub: **rohaan2802**  
Algorithms project — heaps, treaps vs BST, Merkle trees.

Heap work shared with 22i-0894 and 22i-1305. Follow the three rubrics independently for grading.
