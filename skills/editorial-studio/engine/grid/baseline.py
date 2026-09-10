"""
engine/grid/baseline.py
Swiss Modular Grid & Micro-Typography Baseline Locking Engine.

Authoritative Sources:
- ORIGINAL_REQUEST.md §R3
- personas/typographer.md §3, §5, §6
- Bringhurst, The Elements of Typographic Style
- Müller-Brockmann, Grid Systems in Graphic Design
"""

from __future__ import annotations
import math
from typing import Sequence, List, Union


def snap_to_baseline(
    y: float,
    baseline_step: float = 6.0,
    base_pt: float | None = None
) -> float:
    """
    Snaps a continuous vertical coordinate to the nearest baseline grid line.

    Formula:
        y_snapped = floor(y / B + 0.5) * B
    This matches Typst's calc.round(y / B) * B and CSS baseline snapping.

    Args:
        y: Continuous vertical coordinate in points (pt).
        baseline_step: Baseline grid increment B in points (default 6.0pt).
        base_pt: Optional alias for baseline_step.

    Returns:
        Snapped vertical coordinate in points (float).
    """
    b = base_pt if base_pt is not None else baseline_step
    if b <= 0.0:
        raise ValueError(f"Baseline step must be strictly positive, got {b}")

    # Standard positive-shift rounding matching Typst calc.round
    snapped = math.floor(float(y) / b + 0.5) * b
    return round(snapped, 6)


def snap_container_height(
    h: float,
    baseline_step: float = 6.0,
    base_pt: float | None = None
) -> float:
    """
    Snaps a container or figure height upward to an integer multiple of baseline step.
    Prevents vertical clipping and content truncation by always allocating >= natural height.

    Formula:
        h_snapped = ceil(h / B) * B

    Args:
        h: Continuous natural container height in points (pt).
        baseline_step: Baseline grid increment B in points (default 6.0pt).
        base_pt: Optional alias for baseline_step.

    Returns:
        Snapped container height in points (float).
    """
    b = base_pt if base_pt is not None else baseline_step
    if b <= 0.0:
        raise ValueError(f"Baseline step must be strictly positive, got {b}")

    if h <= 0.0:
        return 0.0

    snapped = math.ceil(float(h) / b) * b
    return round(snapped, 6)


def compute_leading(font_size_pt: float, base_pt: float = 6.0) -> float:
    """
    Calculates minimal typographic leading so that (font_size + leading)
    is an integer multiple of the baseline unit base_pt, enforcing a minimum
    leading buffer of 2.0pt.

    Args:
        font_size_pt: Nominal font size in points.
        base_pt: Baseline grid unit in points (default 6.0pt).

    Returns:
        Leading in points.
    """
    if base_pt <= 0.0:
        raise ValueError(f"base_pt must be positive, got {base_pt}")

    line_pitch = math.ceil(font_size_pt / base_pt) * base_pt
    if line_pitch - font_size_pt < 2.0:
        line_pitch += base_pt
    return round(line_pitch - font_size_pt, 6)


def validate_cross_spine_alignment(
    verso_lines: Sequence[float],
    recto_lines: Sequence[float],
    tolerance: float = 0.25
) -> bool:
    """
    Validates horizontal baseline registration across the spine between facing spreads.
    Every corresponding line on Verso and Recto must align within tolerance:
        |y_verso[i] - y_recto[i]| <= tolerance (default 0.25pt).

    Args:
        verso_lines: Sequence of vertical line coordinates on verso (left) page.
        recto_lines: Sequence of vertical line coordinates on recto (right) page.
        tolerance: Maximum acceptable baseline offset in points (default 0.25pt).

    Returns:
        True if all paired lines align within tolerance, False otherwise.
    """
    if not verso_lines or not recto_lines:
        return True

    for v, r in zip(verso_lines, recto_lines):
        if abs(v - r) > tolerance:
            return False

    return True


# Glyph classification sets for optical hanging punctuation
HANGING_QUOTES = frozenset({'“', '”', '‘', '’', '«', '»', '"', "'"})
HANGING_HYPHENS = frozenset({'-', '–', '—', '\u2010', '\u2011', '\u00ad'})
HANGING_PERIODS = frozenset({'.', ',', ';', ':', '…'})


def get_hanging_punctuation_ratio(char: str) -> float:
    """
    Returns the optical hanging protrusion ratio (relative to glyph/em width):
    - Quotes: 100% (1.00)
    - Hyphens, En-dashes, Em-dashes: 75% (0.75)
    - Periods, Commas, Colons, Semicolons: 50% (0.50)
    - Other characters: 0.00
    """
    if not char:
        return 0.0
    c = char[0]
    if c in HANGING_QUOTES:
        return 1.00
    if c in HANGING_HYPHENS:
        return 0.75
    if c in HANGING_PERIODS:
        return 0.50
    return 0.00


def get_hanging_punctuation_offset(char: str, font_size: float) -> float:
    """
    Calculates optical hanging punctuation offset in points:
        offset = ratio * font_size

    Args:
        char: Punctuation glyph string.
        font_size: Type font size in points.

    Returns:
        Offset in points to project outside margin boundary.
    """
    ratio = get_hanging_punctuation_ratio(char)
    return round(ratio * float(font_size), 4)


def detect_orphan_words(line: str) -> bool:
    """
    Returns True if the line contains a single isolated word (1-word orphan defect).
    """
    words = line.strip().split()
    return len(words) == 1


def fix_orphan_line(text: str, nbsp_char: str = "~") -> str:
    """
    Inserts a non-breaking space between the penultimate and terminal word of a paragraph,
    preventing isolated single-word trailing lines (orphans).

    Args:
        text: Paragraph or line string.
        nbsp_char: Non-breaking space character (default '~' for Typst / markdown).

    Returns:
        Sanitized string with penultimate and ultimate words bonded.
    """
    words = text.strip().split()
    if len(words) >= 2:
        if len(words) > 2:
            return " ".join(words[:-2]) + " " + words[-2] + nbsp_char + words[-1]
        return words[0] + nbsp_char + words[1]
    return text


def validate_paragraph_split(
    lines_page_1: int,
    lines_page_2: int,
    min_widow: int = 2
) -> List[str]:
    """
    Validates a paragraph split across column or page breaks against Bringhurst widow/orphan rules.
    Enforces that at least min_widow lines remain on page 1 and at least min_widow lines carry to page 2.

    Args:
        lines_page_1: Number of lines left on the preceding page/column.
        lines_page_2: Number of lines carried to the subsequent page/column.
        min_widow: Minimum allowable lines on either side of the break (default 2).

    Returns:
        List of error description strings (empty if compliant).
    """
    errors: List[str] = []
    if lines_page_1 < min_widow:
        errors.append(
            f"Orphan line error: only {lines_page_1} line(s) left on first page (minimum is {min_widow})"
        )
    if lines_page_2 < min_widow:
        errors.append(
            f"Widow line error: only {lines_page_2} line(s) carried forward to next page (minimum is {min_widow})"
        )
    return errors


def sanitize_text_widows_orphans(
    text: str,
    nbsp_char: str = "~",
    min_lines: int = 2
) -> str:
    """
    Sanitizes narrative text for publication:
    1. Replaces standard space between penultimate and ultimate words with a non-breaking space
       per paragraph to eliminate 1-word orphans.
    2. Preserves paragraph structure and line breaks.

    Args:
        text: Raw narrative text string.
        nbsp_char: Non-breaking space delimiter (default '~').
        min_lines: Widow/orphan minimum line threshold (default 2).

    Returns:
        Sanitized text string.
    """
    if not text:
        return ""

    # Split into paragraphs by double newlines or single newlines
    paragraphs = text.split("\n\n")
    sanitized_paragraphs = []

    for para in paragraphs:
        lines = para.split("\n")
        sanitized_lines = []
        for line in lines:
            if line.strip():
                sanitized_lines.append(fix_orphan_line(line, nbsp_char=nbsp_char))
            else:
                sanitized_lines.append(line)
        sanitized_paragraphs.append("\n".join(sanitized_lines))

    return "\n\n".join(sanitized_paragraphs)
