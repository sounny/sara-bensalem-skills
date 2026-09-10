"""
engine package for editorial-studio publishing system.
Provides grid calculus, ISO 128 drafting, dual-engine compilation (Typst + Paged.js),
and unified compilation CLI.
"""

from typing import Any, Dict, Optional


def compile_document(
    input_path: str,
    output_path: Optional[str] = None,
    engine: str = "auto",
    bleed: str = "3mm",
    profile: str = "FOGRA51",
    benchmark: bool = False,
    timeout_sec: float = 30.0,
    **kwargs
) -> Dict[str, Any]:
    """Lazy wrapper for unified compilation dispatcher."""
    from engine.compile import compile_document as _compile_doc
    return _compile_doc(
        input_path=input_path,
        output_path=output_path,
        engine=engine,
        bleed=bleed,
        profile=profile,
        benchmark=benchmark,
        timeout_sec=timeout_sec,
        **kwargs
    )


def compile_typst(input_path: str, output_path: str, timeout_sec: float = 10.0, **kwargs) -> Dict[str, Any]:
    """Lazy wrapper for Typst compilation."""
    from engine.typst.build_typst import compile_typst as _compile_typ
    return _compile_typ(input_path, output_path, timeout_sec=timeout_sec, **kwargs)


def compile_pagedjs(input_html: str, output_pdf: str, timeout_sec: float = 30.0, **kwargs) -> Dict[str, Any]:
    """Lazy wrapper for Paged.js compilation."""
    from engine.pagedjs.build_pagedjs import compile_pagedjs as _compile_paged
    return _compile_paged(input_html, output_pdf, timeout_sec=timeout_sec, **kwargs)


__all__ = ["compile_document", "compile_typst", "compile_pagedjs"]
