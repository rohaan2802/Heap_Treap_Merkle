"""Stream JSON Lines from a compressed Reddit submission dump."""

import io
import json


def stream_reddit_zst(filepath, max_rows=None):
    """Yield (post ID, timestamp, score) without loading the dump into memory."""
    if max_rows is not None and max_rows < 0:
        raise ValueError("max_rows must be nonnegative")
    if max_rows == 0:
        return

    import zstandard

    count = 0
    with open(filepath, "rb") as source:
        with zstandard.ZstdDecompressor().stream_reader(source) as reader:
            with io.TextIOWrapper(reader, encoding="utf-8") as text:
                for line in text:
                    try:
                        row = json.loads(line)
                        post = row["id"], int(row["created_utc"]), int(row.get("score", 0))
                    except (KeyError, ValueError, TypeError, AttributeError):
                        continue
                    yield post
                    count += 1
                    if count == max_rows:
                        return
