#!/usr/bin/env python3
"""One-line joke: an excuse for missing a deadline.

Competition: u-markk-st-one-line-no-deadline-met-6adc00ce
The entry is the single line below and nothing else.
"""

import os
import sys

ENTRY = "I didn't miss the deadline \u2014 I was just giving it space. Healthy relationships need boundaries, and mine clearly needed a weekend."

MAX_CHARS = 200


def validate(entry: str) -> None:
    if not entry:
        raise ValueError("entry must not be empty")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    if len(entry) > MAX_CHARS:
        raise ValueError("entry exceeds 200 characters")
    if entry != entry.strip():
        raise ValueError("entry has stray leading/trailing whitespace")
    if len(entry.encode("utf-8")) == 0:
        raise ValueError("entry must contain text")


def verify_roundtrip(entry: str) -> None:
    """Stage the entry to a temp file and read it back to prove integrity."""
    import tempfile

    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", delete=False, suffix=".txt"
    ) as tmp:
        tmp.write(entry)
        tmp_path = tmp.name
    try:
        with open(tmp_path, encoding="utf-8") as f:
            staged = f.read()
        if staged != entry:
            raise ValueError("round-trip verification failed")
    finally:
        os.unlink(tmp_path)


def main() -> int:
    validate(ENTRY)
    verify_roundtrip(ENTRY)
    try:
        sys.stdout.write(ENTRY)
        sys.stdout.flush()
    except Exception:
        # Fallback: stdout unavailable, persist the entry to a file instead.
        out = os.environ.get("MAKEFUN_OUTPUT") or "./output/entry.txt"
        parent = os.path.dirname(out)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(ENTRY)
        # Re-verify what was written matches the entry exactly.
        with open(out, encoding="utf-8") as f:
            if f.read() != ENTRY:
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
