"""Pigeon Pitch, One Line: a city pigeon's elevator pitch for investors.

The entry is one line, at most 200 characters: a city pigeon pitching
its breadcrumb startup to investors. This program writes that pitch,
byte for byte, to /output/entry.txt and then reads it back to prove
the file holds exactly the locked pitch and nothing else.
"""

import os
import sys
from pathlib import Path

PITCH = "We are Uber, but for breadcrumbs: one tap and three hundred pigeons arrive before your sandwich hits the pavement."

CHAR_LIMIT = 200
EM_DASH = "\u2014"


def is_good(line: str) -> bool:
    """Gate: 1-200 chars, one line, no em dash, not only whitespace."""
    if not line or line.strip() == "":
        return False
    if len(line) > CHAR_LIMIT:
        return False
    if line != line.strip():
        return False
    if "\n" in line or "\r" in line:
        return False
    if EM_DASH in line:
        return False
    return True


def produce(out_dir: Path) -> Path:
    """Write the locked pitch to entry.txt, readable by everyone."""
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(PITCH, encoding="utf-8")
    os.chmod(target, 0o644)
    return target


def check_entry(target: Path) -> None:
    """Re-read entry.txt and prove it is exactly the locked pitch."""
    data = target.read_bytes()
    text = data.decode("utf-8")
    if text != PITCH:
        raise SystemExit("entry.txt is not the locked pitch")
    if not is_good(text):
        raise SystemExit("entry.txt fails the gate")
    if data != PITCH.encode("utf-8"):
        raise SystemExit("entry.txt bytes are not exactly the locked pitch")
    if b"\t" in data:
        raise SystemExit("entry.txt must not contain a tab")
    if len(data) != len(PITCH.encode("utf-8")):
        raise SystemExit("entry.txt byte length does not match the pitch")
    if data.endswith(b"\n"):
        raise SystemExit("entry.txt must not end with a newline")
    if (target.stat().st_mode & 0o777) != 0o644:
        raise SystemExit("entry.txt must be mode 0644")


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target = produce(out_dir)
    check_entry(target)
    print("wrote %s (%d chars)" % (target, len(PITCH)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
