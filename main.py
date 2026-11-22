#!/usr/bin/env python3
"""Deliver the Twenty-Two front page.

`build_art.py` paints entry.png; this file is the delivery step. It
copies the painted page into the directory the harness reads and
refuses to deliver anything unless the bytes are exactly the page the
painter produced: right format, right size, right fingerprint.

Standard library only, so it runs in the grader's pinned image with
no fonts and no third-party packages.

Usage:
    python3 main.py            # writes entry.png to /output by default
    MAKEFUN_OUTPUT_DIR=out python3 main.py   # or to the given directory
"""

import hashlib
import os
import pathlib
import shutil
import sys

# Fingerprint of entry.png exactly as build_art.py paints it -- repaint
# and this value changes, so delivery refuses the new bytes until it
# is updated here.
WANT = "e0cad4200309243270355275a80628a7794d3974a3cc1fafd10f359ab42661e0"
CEILING = 1048576
MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("twenty-two: " + message, file=sys.stderr)
    return 1


def check_blob(blob):
    """Verify the delivered bytes are the painted page; 0 means good."""
    if len(blob) > CEILING:
        return fail("entry.png is %d bytes, over the 1 MiB ceiling"
                    % len(blob))
    if blob[:8] != MAGIC:
        return fail("entry.png is not a PNG file")
    got = hashlib.sha256(blob).hexdigest()
    if got != WANT:
        return fail("fingerprint mismatch: got %s" % got)
    return 0


def run():
    root = pathlib.Path(__file__).resolve().parent
    source = root / "entry.png"
    if not source.exists():
        return fail("entry.png is missing -- run build_art.py first")
    out_dir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    blob = target.read_bytes()
    problem = check_blob(blob)
    if problem:
        return problem
    print("twenty-two: wrote %s (%d bytes, sha256 %s)"
          % (target, len(blob), hashlib.sha256(blob).hexdigest()))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
