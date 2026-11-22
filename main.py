#!/usr/bin/env python3
"""Ship the Twenty-Two front page to the grader.

`build_art.py` paints entry.png; this file is the ship step. It copies
the painted page into the directory the harness reads, and it will not
ship anything unless the bytes are exactly the page the painter made:
right format, right size, right fingerprint.

Pure standard library, so it runs in the grader's pinned image with
no fonts and no third-party packages.

    python3 main.py            # writes entry.png to /output by default
    MAKEFUN_OUTPUT_DIR=out python3 main.py   # or to the given directory
"""

import hashlib
import os
import pathlib
import shutil
import struct
import sys

# Fingerprint of entry.png exactly as build_art.py paints it. Repaint
# and this value changes, so shipping refuses the new bytes until the
# fingerprint here is updated to match.
EXPECTED_SHA256 = "e0cad4200309243270355275a80628a7794d3974a3cc1fafd10f359ab42661e0"
MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def complain(text):
    print("twenty-two: " + text, file=sys.stderr)
    return 1


def blob_ok(blob):
    """Check the bytes are the painted page; 0 means they are."""
    if len(blob) > MAX_BYTES:
        return complain("entry.png is %d bytes, over the 1 MiB ceiling"
                        % len(blob))
    if blob[:8] != PNG_MAGIC:
        return complain("entry.png is not a PNG file")
    if len(blob) < 33 or blob[12:16] != b"IHDR":
        return complain("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", blob[16:24])
    if width > 1024 or height > 1024:
        return complain("entry.png is %dx%d, over the 1024x1024 ceiling"
                        % (width, height))
    digest = hashlib.sha256(blob).hexdigest()
    if digest != EXPECTED_SHA256:
        return complain("fingerprint mismatch: got %s" % digest)
    return 0


def ship():
    here = pathlib.Path(__file__).resolve().parent
    painted = here / "entry.png"
    if not painted.exists():
        return complain("entry.png is missing -- run build_art.py first")
    dest_dir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    shutil.copyfile(painted, dest)
    data = dest.read_bytes()
    bad = blob_ok(data)
    if bad:
        return bad
    print("twenty-two: wrote %s (%d bytes, sha256 %s)"
          % (dest, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    raise SystemExit(ship())
