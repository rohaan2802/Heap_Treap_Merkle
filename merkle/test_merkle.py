import unittest
import time
from merkle.merkle import MerkleTree

class TestMerkleSystem(unittest.TestCase):

    def setUp(self):
        """Setup a small dataset for testing logic."""
        self.sample_data = [
            {"id": "R1", "asin": "A1", "rating": 5, "text": "great"},
            {"id": "R2", "asin": "A2", "rating": 1, "text": "bad"},
            {"id": "R3", "asin": "A3", "rating": 3, "text": "ok"},
            {"id": "R4", "asin": "A4", "rating": 2, "text": "poor"}
        ]
        self.tree = MerkleTree(self.sample_data)
        self.root = self.tree.build_tree()

    def test_tree_construction_basic(self):
        """Test if tree builds without error and returns a hash."""
        self.assertIsNotNone(self.root)
        self.assertEqual(len(self.root), 64) # SHA256 length

    def test_consistency(self):
        """Rubric: Load same dataset twice, root must be identical."""
        tree2 = MerkleTree(self.sample_data)
        root2 = tree2.build_tree()
        self.assertEqual(self.root, root2)

    def test_tamper_modification(self):
        """Rubric: Detect modification."""
        bad_data = [d.copy() for d in self.sample_data]
        bad_data[0]['text'] = "hacked"

        bad_tree = MerkleTree(bad_data)
        bad_root = bad_tree.build_tree()
        self.assertNotEqual(self.root, bad_root)

    def test_tamper_deletion(self):
        """Rubric: Detect deletion."""
        bad_data = self.sample_data[1:] # Remove first item
        bad_tree = MerkleTree(bad_data)
        bad_root = bad_tree.build_tree()
        self.assertNotEqual(self.root, bad_root)

    def test_tamper_insertion(self):
        """Rubric: Detect insertion."""
        bad_data = self.sample_data[:]
        bad_data.append({"id": "R5", "asin": "A5", "rating": 5, "text": "fake"})
        bad_tree = MerkleTree(bad_data)
        bad_root = bad_tree.build_tree()
        self.assertNotEqual(self.root, bad_root)

    def test_proof_validity(self):
        """Rubric: Proof path verifies correctly."""
        idx = 0
        leaf = self.tree.leaves[idx]
        proof = self.tree.generate_proof(idx)

        # Should return True
        is_valid = self.tree.verify_proof(leaf, proof, self.root)
        self.assertTrue(is_valid)

    def test_proof_performance(self):
        """Rubric: Proof verification < 100ms."""
        idx = 0
        leaf = self.tree.leaves[idx]
        proof = self.tree.generate_proof(idx)

        start = time.time()
        self.tree.verify_proof(leaf, proof, self.root)
        end = time.time()

        duration_ms = (end - start) * 1000
        self.assertLess(duration_ms, 100)
        print(f"\n[TEST] Proof Time: {duration_ms:.4f} ms")

if __name__ == '__main__':
    print("Running Merkle Logic Tests...")
    unittest.main()
