# ======= experiments.py =======
# Experiment helpers to compare BST and Treap on:
# - insertion time
# - search time (getMostPopular)
# - deletion time
# - height
# - balancing factor
# - rotations (Treap only)

import time
import math
import random
from .trees import BSTFeed, TreapFeed


def compute_balancing_factor(height, n):
    """
    Simple 'balancing factor':
    ratio = height / log2(n)
    - Perfectly balanced tree ≈ small ratio (~1–2)
    - Very skewed tree (like linked list) ≫ 1
    """
    if n <= 1:
        return 0.0
    return height / math.log2(n)


def run_single_structure(feed_cls, posts, n_search=100, delete_ratio=0.1):
    """
    Build one structure (BST or Treap), run operations, and measure metrics.

    feed_cls: BSTFeed or TreapFeed
    posts: list of (post_id, timestamp, score)
    n_search: how many times to call getMostPopular()
    delete_ratio: fraction of posts to delete (e.g. 0.1 = 10%)
    """
    feed = feed_cls()
    n = len(posts)

    # ----- insertion timing -----
    insert_times = []
    for pid, ts, sc in posts:
        t0 = time.perf_counter()
        feed.addPost(pid, ts, sc)
        t1 = time.perf_counter()
        insert_times.append(t1 - t0)

    # ----- search timing (getMostPopular) -----
    search_times = []
    for _ in range(n_search):
        t0 = time.perf_counter()
        _ = feed.getMostPopular()
        t1 = time.perf_counter()
        search_times.append(t1 - t0)

    height = feed.height()
    rotations = getattr(feed, "rotation_count", 0)

    # ----- deletion timing -----
    delete_times = []
    ids = [p[0] for p in posts]
    random.Random(42).shuffle(ids)
    num_delete = int(delete_ratio * n)

    for pid in ids[:num_delete]:
        t0 = time.perf_counter()
        feed.deletePost(pid)
        t1 = time.perf_counter()
        delete_times.append(t1 - t0)

    balancing = compute_balancing_factor(height, n)

    return {
        "structure": feed_cls.__name__.replace("Feed", ""),  # "BST" or "Treap"
        "n_posts": n,
        "avg_insert_time": sum(insert_times) / len(insert_times) if insert_times else 0.0,
        "avg_search_time": sum(search_times) / len(search_times) if search_times else 0.0,
        "avg_delete_time": sum(delete_times) / len(delete_times) if delete_times else 0.0,
        "height": height,
        "balancing_factor": balancing,
        "rotations": rotations,
    }


def run_experiments_for_sizes(all_posts, sizes, n_search=100, delete_ratio=0.1):
    """
    Run experiments for different sample sizes on both BST and Treap.

    Returns: list of metrics dicts (rows) for all runs.
    """
    rows = []
    for N in sizes:
        subset = all_posts[:N]
        rows.append(run_single_structure(BSTFeed, subset, n_search, delete_ratio))
        rows.append(run_single_structure(TreapFeed, subset, n_search, delete_ratio))
    return rows


def compare_on_posts(posts, n_search=100, delete_ratio=0.1):
    """
    Helper for quick tests:
    runs BST and Treap on the same posts and returns two rows of metrics.
    """
    rows = []
    rows.append(run_single_structure(BSTFeed, posts, n_search=n_search, delete_ratio=delete_ratio))
    rows.append(run_single_structure(TreapFeed, posts, n_search=n_search, delete_ratio=delete_ratio))
    return rows
