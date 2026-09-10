"""
engine.typst package for editorial-studio publishing system.
Provides declarative Typst templates and compilation pipeline.
"""

from typing import Any, Dict


def compile_typst(input_path: str, output_path: str, timeout_sec: float = 10.0, **kwargs) -> Dict[str, Any]:
    """Lazy wrapper to import and execute compile_typst without runpy package collisions."""
    from engine.typst.build_typst import compile_typst as _compile
    return _compile(input_path, output_path, timeout_sec=timeout_sec, **kwargs)


__all__ = ["compile_typst"]
