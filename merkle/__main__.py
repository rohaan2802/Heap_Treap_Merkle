"""Show review integrity and inclusion checks against a trusted root."""

import argparse
from .merkle import CLI, MerkleTree, ReviewDataset, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reviews", nargs="?", help="JSON Lines file; omit for the interactive menu")
    args = parser.parse_args()
    if args.reviews is None:
        CLI().run()
        return
    data = ReviewDataset()
    data.load_json(args.reviews)
    if not data.records:
        parser.error("no reviews found")
    tree = MerkleTree(data.records)
    root = tree.build_tree()
    index = len(data.records) - 1
    proof = tree.generate_proof(index)
    valid = tree.verify_proof(tree.leaves[index], proof, root)
    invalid = tree.verify_proof(sha256("changed record"), proof, root)
    modified = data.records[:]
    modified[index] = dict(modified[index], text=modified[index]["text"] + " [edited]")
    print(f"\nReviews     : {len(data.records)}")
    print(f"Root SHA-256: {root}")
    print(f"Review proof: {data.records[index]['id']} ({len(proof)} sibling hashes)")
    print(f"Original proof accepted : {valid}")
    print(f"Changed leaf accepted   : {invalid}")
    print(f"Editing text changes root: {MerkleTree(modified).build_tree() != root}")


if __name__ == "__main__":
    main()
