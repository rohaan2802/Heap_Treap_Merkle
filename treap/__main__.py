"""Compare feed structures on a deterministic, chronological workload."""

import argparse
import random

from .dataset_utils import stream_reddit_zst
from .experiments import run_experiments_for_sizes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--posts", type=int, default=1000, help="maximum posts to read")
    parser.add_argument("--dataset", help="optional Reddit JSON Lines .zst file")
    args = parser.parse_args()
    if args.posts < 1:
        parser.error("--posts must be positive")
    random.seed(42)
    rng = random.Random(42)
    if args.dataset:
        try:
            posts = list(stream_reddit_zst(args.dataset, args.posts))
        except (OSError, ImportError) as error:
            parser.error(str(error))
    else:
        posts = [(f"post-{i}", i, rng.randrange(1000)) for i in range(args.posts)]
    if not posts:
        parser.error("no posts found")
    sizes = sorted({max(1, len(posts) // 4), max(1, len(posts) // 2), len(posts)})
    print("Dataset:", args.dataset or "synthetic chronological feed (seed 42)")
    print("Height is measured before deletion; timings are means.")
    print("\nPosts   Tree       Height  Rotations   Insert us  Popular us  Delete us")
    for row in run_experiments_for_sizes(posts, sizes):
        print(f"{row['n_posts']:>5}   {row['structure']:<7} {row['height']:>8}"
              f" {row['rotations']:>10} {row['avg_insert_time']*1e6:>11.2f}"
              f" {row['avg_search_time']*1e6:>11.2f} {row['avg_delete_time']*1e6:>10.2f}")


if __name__ == "__main__":
    main()
