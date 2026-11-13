#!/usr/bin/env python3
"""
MERKLE TREE INTEGRITY SYSTEM (Final Version)
- Logic: SHA-256 on 4 Selected Columns.
- Storage: Saves root to 'trusted_root.txt' (Deleted on Exit).
- Tamper Flow: Modify -> Save to JSON -> Reload from JSON -> Recalculate -> Detect.
"""

import os
import json
import time
import hashlib
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple, Optional

# ==================================================================
# 1. DATA PREPROCESSING
# ==================================================================

class ReviewDataset:
    def __init__(self):
        self.records = []
        self.id_index = {}

    def load_json(self, path: str, limit: Optional[int] = None):
        print(f"[INFO] Loading dataset from: {path}")
        start = time.time()

        self.records = [] # Clear existing data
        self.id_index = {}
        count = 0

        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if limit is not None and count >= limit:
                        break
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if not isinstance(obj, dict):
                        continue

                    # Extract the four fields covered by the proof.
                    review_id = obj.get("review_id") or obj.get("reviewerID") or f"GEN_ID_{count}"
                    asin = obj.get("asin", "UNKNOWN")
                    raw_text = obj.get("reviewText", "")
                    rating = obj.get("overall", 0)

                    clean_text = raw_text if isinstance(raw_text, str) else ""

                    record = {
                        "id": review_id,
                        "asin": asin,
                        "rating": rating,
                        "text": clean_text
                    }

                    self.records.append(record)
                    self.id_index[review_id] = count
                    count += 1
        except FileNotFoundError:
            print(f"[ERROR] File not found: {path}")
            return

        elapsed = time.time() - start
        print(f"[INFO] Successfully loaded {len(self.records)} records in {elapsed:.2f}s")

    def save_to_json(self, path: str):
        """Saves current memory records back to a JSON file."""
        print(f"[DISK I/O] Saving {len(self.records)} records to {path}...")
        start = time.time()

        with open(path, "w", encoding="utf-8") as f:
            for r in self.records:
                # Reconstruct a JSON object compatible with the loader
                obj = {
                    "reviewerID": r['id'],
                    "asin": r['asin'],
                    "overall": r['rating'],
                    "reviewText": r['text']
                }
                f.write(json.dumps(obj) + "\n")

        print(f"[DISK I/O] Save complete in {time.time() - start:.2f}s")

# ==================================================================
# 2. MERKLE TREE CONSTRUCTION
# ==================================================================

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

class MerkleTree:
    def __init__(self, records: List[dict]):
        self.records = records
        self.leaves = []
        self.levels = []
        self.root = None

    def build_tree(self) -> Optional[str]:
        if not self.records:
            self.leaves, self.levels = [], []
            self.root = None
            return None

        # 1. Hash Leaves (Selected Columns)
        self.leaves = []
        for r in self.records:
            data_str = "leaf:" + json.dumps([r["id"], r["asin"], r["rating"], r["text"]],
                                             ensure_ascii=False, separators=(",", ":"))
            self.leaves.append(sha256(data_str))

        self.levels = [self.leaves]
        current_level = self.leaves

        # 2. Build Upwards
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i+1] if (i+1) < len(current_level) else left
                combined = sha256("node:" + left + right)
                next_level.append(combined)

            self.levels.append(next_level)
            current_level = next_level

        self.root = sha256(f"root:{len(self.leaves)}:" + current_level[0])
        return self.root

    def generate_proof(self, index: int) -> List[Tuple[str, str]]:
        if not 0 <= index < len(self.leaves):
            raise IndexError("leaf index out of range")
        proof = []
        for level in self.levels[:-1]:
            is_right_child = (index % 2) == 1
            sibling_index = index - 1 if is_right_child else index + 1
            if sibling_index >= len(level):
                sibling_hash = level[index]
            else:
                sibling_hash = level[sibling_index]
            direction = "L" if is_right_child else "R"
            proof.append((sibling_hash, direction))
            index //= 2
        return proof

    def verify_proof(self, leaf_hash: str, proof: List[Tuple[str, str]], target_root: str, *, leaf_count: Optional[int] = None) -> bool:
        computed_hash = leaf_hash
        for sibling, direction in proof:
            if direction == "L":
                computed_hash = sha256("node:" + sibling + computed_hash)
            elif direction == "R":
                computed_hash = sha256("node:" + computed_hash + sibling)
            else:
                return False
        count = len(self.leaves) if leaf_count is None else leaf_count
        return count > 0 and sha256(f"root:{count}:" + computed_hash) == target_root

# ==================================================================
# 3. PERFORMANCE & ANALYTICS
# ==================================================================

class PerformanceStats:
    @staticmethod
    def run_scaling_test(dataset: ReviewDataset):
        print("\n--- RUNNING SCALING ANALYSIS ---")
        full_data = dataset.records
        sizes = [1000, 10000, 50000, 100000, 1000000]
        print(f"{'Records':<10} | {'Build Time (s)':<15}")
        print("-" * 30)
        for size in sizes:
            if size > len(full_data): break
            subset = full_data[:size]
            t0 = time.time()
            temp_tree = MerkleTree(subset)
            temp_tree.build_tree()
            t1 = time.time()
            print(f"{size:<10} | {t1-t0:<15.4f}")

# ==================================================================
# 4. CLI INTERFACE
# ==================================================================

class CLI:
    def __init__(self):
        self.dataset = ReviewDataset()
        self.tree = None
        self.workspace = tempfile.TemporaryDirectory(prefix="merkle-")
        self.root_filename = Path(self.workspace.name) / "trusted_root.txt"
        self.tamper_filename = Path(self.workspace.name) / "tampered_dataset.json"

    def save_root_to_file(self, root_hash: str):
        with open(self.root_filename, "w") as f:
            f.write(root_hash)
        print(f"[INFO] Trusted Root saved to: {self.root_filename}")

    def get_stored_root(self):
        if not os.path.exists(self.root_filename):
            return None
        with open(self.root_filename, "r") as f:
            return f.read().strip()

    def display_data_table(self):
        if not self.dataset.records:
            print("[WARN] No data loaded.")
            return
        print("\n--- DATASET PREVIEW (First 5) ---")
        print(f"{'Review ID':<20} | {'Text Snippet'}")
        print("-" * 60)
        for r in self.dataset.records[:5]:
            snippet = (r['text'][:40] + '...') if len(r['text']) > 40 else r['text']
            print(f"{r['id']:<20} | {snippet}")

    def run(self):
        while True:
            print("\n" + "="*50)
            print("   MERKLE TREE INTEGRITY SYSTEM")
            print("="*50)
            print("1. Load Dataset")
            print("2. View Dataset")
            print("3. Build Merkle Tree")
            print("4. Save Trusted Root (to TXT file)")
            print("5. Verify Integrity")
            print("6. Generate Inclusion Proof")
            print("7. Simulate Tampering (Save JSON -> Reload)")
            print("8. Run Benchmarks")
            print("9. Exit")

            choice = input("\nSelect Option: ")

            if choice == "1":
                path = input("Enter file path: ")
                limit_str = input("Limit records (Enter for None): ")
                try:
                    limit = int(limit_str) if limit_str.strip() else None
                    if limit is not None and limit < 1:
                        raise ValueError
                except ValueError:
                    print("Enter a positive record limit, or leave it blank.")
                    continue
                self.tree = None
                self.dataset.load_json(path, limit)

            elif choice == "2":
                self.display_data_table()

            elif choice == "3":
                if not self.dataset.records:
                    print("[ERROR] Load data first.")
                    continue
                self.tree = MerkleTree(self.dataset.records)
                root = self.tree.build_tree()
                print(f"\n[SUCCESS] Merkle Root Generated:\n{root}")

            elif choice == "4":
                if self.tree and self.tree.root:
                    self.save_root_to_file(self.tree.root)
                else:
                    print("[ERROR] Build tree first.")

            elif choice == "5":
                stored = self.get_stored_root()
                if not stored:
                    print("[ERROR] No saved root file found. Use Option 4.")
                elif not self.tree:
                    print("[ERROR] No current tree built.")
                elif self.tree.root == stored:
                    print("\n[OK] INTEGRITY CONFIRMED: Roots Match.")
                else:
                    print("\n[ERROR] SECURITY ALERT: Roots Do Not Match!")

            elif choice == "6":
                if not self.tree:
                    print("Build tree first."); continue
                rid = input("Enter Review ID to verify: ")
                idx = self.dataset.id_index.get(rid)
                if idx is None:
                    print("[RESULT] ID not found.")
                else:
                    t0 = time.time()
                    proof = self.tree.generate_proof(idx)
                    leaf = self.tree.leaves[idx]
                    ok = self.tree.verify_proof(leaf, proof, self.tree.root)
                    print(f"Valid: {ok} (Time: {(time.time()-t0)*1000:.4f} ms)")

            elif choice == "7":
                self.simulate_tamper_process()

            elif choice == "8":
                if self.dataset.records: PerformanceStats.run_scaling_test(self.dataset)
                else: print("Load data first.")

            elif choice == "9":
                print("Exiting...")
                break

    def simulate_tamper_process(self):
        stored_root = self.get_stored_root()
        if not stored_root or not self.dataset.records:
            print("[ERROR] Save a trusted root (Option 4) first!")
            return

        print("\n--- TAMPER SIMULATION ---")

        # 1. Modify in Memory
        first_record = self.dataset.records[0]
        print(f"Check at the first line (ID: {first_record['id']})")
        print(f"Original Text: {first_record['text'][:50]}...")

        first_record['text'] += " [HACKED]"
        print(f"I have modified this: {first_record['text'][:60]}...")

        # 2. Save to JSON (Simulating persistence)
        print("\n[ACTION] Saving modified data to 'tampered_dataset.json'...")
        self.dataset.save_to_json(self.tamper_filename)

        # 3. Wipe Memory
        print("[ACTION] Wiping system memory...")
        self.dataset.records = []
        self.tree = None

        # 4. Reload from JSON
        print("\n[ACTION] Reloading from 'tampered_dataset.json'...")
        self.dataset.load_json(self.tamper_filename)

        # 5. Recalculate Hash
        print("\n[ACTION] Recalculating the hash...")
        self.tree = MerkleTree(self.dataset.records)
        new_root = self.tree.build_tree()

        # 6. Compare
        print("\n--- RESULTS ---")
        print(f"Previous Saved Root (from txt): {stored_root}")
        print(f"New Calculated Root:            {new_root}")

        if new_root != stored_root:
            print("\n[ALERT] Data is Tampered!")
        else:
            print("\n[?] Error: No change detected.")

if __name__ == "__main__":
    cli = CLI()
    cli.run()
