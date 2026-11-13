# Data

- [sample.road-d](sample.road-d) is an undirected weighted edge list using zero-based vertex IDs: `from to weight`.
- [sample-reviews.jsonl](sample-reviews.jsonl) has three example reviews. The loader accepts `review_id` or `reviewerID`, `asin`, `overall`, and `reviewText`.
- The road release archive contains `Hongkong.road-d`, `Chongqing.road-d`, `Shanghai.road-d`, and `ShanghaiNew.road-D`. Extract it into `data/` and pass the path you want to the heap benchmark.
- The optional Reddit workload expects a `.zst` archive of JSON Lines with `id`, `created_utc`, and `score`. Install the packages in [treap/requirements.txt](../treap/requirements.txt) and run `python -m treap --dataset data/RC_2019-04.zst --posts 10000`. The synthetic demo works without this archive.
