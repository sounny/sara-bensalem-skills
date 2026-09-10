"""
engine.pagedjs package for editorial-studio publishing system.
Provides W3C CSS Paged Media templates, styles, and browser compilation pipeline.
"""

from typing import Any, Dict


def compile_pagedjs(input_html: str, output_pdf: str, timeout_sec: float = 30.0, **kwargs) -> Dict[str, Any]:
    """Lazy wrapper to import and execute compile_pagedjs without runpy package collisions."""
    from engine.pagedjs.build_pagedjs import compile_pagedjs as _compile
    return _compile(input_html, output_pdf, timeout_sec=timeout_sec, **kwargs)


__all__ = ["compile_pagedjs"]
