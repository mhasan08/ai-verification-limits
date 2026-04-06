from __future__ import annotations

import gzip
import lzma
import zlib
from typing import Dict


def estimate_complexity(encoded: str) -> Dict[str, int]:
    """
        Compression-based proxy for description length.
        This is not true Kolmogorov complexity; it is a practical illustration.
    """
    raw = encoded.encode("utf-8")
    return {
        "raw_bytes": len(raw),
        "zlib_bytes": len(zlib.compress(raw)),
        "gzip_bytes": len(gzip.compress(raw)),
        "lzma_bytes": len(lzma.compress(raw)),
    }
