# Heap_Treap_Merkle

Algorithms project package covering **heaps**, **treaps vs BSTs**, and **Merkle trees**: problem statements, rubrics, written reports, screenshots, and Jupyter notebooks that compare treap and BST behavior on Reddit-feed-style workloads (with optional Kaggle dataset metadata).

**Folder:** `ALGO_PROJECT` · Includes collaborative heap zip (`22i-0894_22i-2327_22i-1305_HEAP.zip`)

---

## Overview

This repository aggregates Algorithm course deliverables:

1. **Heap part** - project statement, rubric, and submission zip(s).
2. **Treap part** - algorithm notes (`Project Algorithm - Treaps.pdf`), rubrics, and **Treap vs BST** experimental report + notebooks.
3. **Merkle trees part** - dedicated rubric and evaluation materials.
4. Supporting problem sets (`Problem1.docx`, `Problem2.docx`, `Problem 3.pdf`) and figure exports (`download1.png` ... `download8.png`).

The notebooks (`treap-vs-bst-reddit-feed.ipynb` and the updated variant) implement and measure tree structures against feed-like insert/query patterns.

---

## Features

- Side-by-side **treap vs balanced/unbalanced BST** analysis with PDF/DOCX reports
- Jupyter notebooks ready for interactive reproduction
- Kaggle upload scaffolding (`kaggle_upload/dataset-metadata.json`, `sda.txt`)
- Rubrics for heap, treap, and Merkle tree grading components
- Archived source zips for section-specific submissions

---

## Repository structure

```text
Heap_Treap_Merkle/
├── 22i_2327_A3_Sec_D.zip
└── ALGO_PROJECT/
    ├── treap-vs-bst-reddit-feed.ipynb
    ├── treap-vs-bst-reddit-feed-updated.ipynb
    ├── Treap_vs_BST_Report.pdf / .docx
    ├── Project Algorithm - Treaps.pdf
    ├── Project Statement - Heap Part.zip
    ├── Rubric - Heap Part.pdf
    ├── Rubric - Treap Part.pdf
    ├── Rubric - Merkle Trees Part.pdf
    ├── Rubric evaluation summary.pdf
    ├── Problem1.docx | Problem2.docx | Problem 3.pdf
    ├── kaggle_upload/
    │   ├── dataset-metadata.json
    │   └── sda.txt
    ├── 22i-0894_22i-2327_22i-1305_HEAP.zip
    └── *.png / Capture.PNG / ...
```

---

## Build / run

### Notebooks

```bash
cd ALGO_PROJECT
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install jupyter notebook matplotlib numpy pandas
jupyter notebook treap-vs-bst-reddit-feed-updated.ipynb
```

Or open the `.ipynb` files directly in VS Code / JupyterLab.

### Reports & zips

- Open PDFs/DOCX with a standard viewer.
- Extract `*_HEAP.zip` / section zips to inspect language-specific heap implementations used for submission.

### Optional Kaggle publish

Follow `kaggle_upload/sda.txt` (set `KAGGLE_API_TOKEN`, then `kaggle datasets create -p .`). Replace any placeholder token before use.

---

## Usage

1. Read the relevant rubric before modifying code so deliverables stay aligned.
2. Run the updated notebook for the latest treap-vs-BST measurements and charts.
3. Cross-check figures in the report against notebook outputs (`download*.png`).

---

## Extending

- Add Merkle proof verification demos as a companion notebook.
- Parameterize treap priorities / BST insert orders for stress tests.
- Benchmark against larger SNAP or Reddit dump samples and commit a results CSV.

---

## License

Academic project materials - notebooks may depend on third-party data; respect those licenses (metadata lists CC0 for the archive dataset stub).
