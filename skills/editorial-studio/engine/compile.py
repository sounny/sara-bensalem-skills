"""
engine/compile.py
Unified Dual-Engine Compilation CLI & Dispatcher for editorial-studio publishing system.
Orchestrates high-speed declarative Typst builds alongside W3C CSS Paged Media web-to-print.
Conforms to ORIGINAL_REQUEST.md §R2, PROJECT.md §Code Layout, and SKILL.md §CLI Build Procedures.
"""

import os
import sys
import time
import argparse
import json
import re
from typing import Dict, Any, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engine.typst.build_typst import compile_typst
from engine.pagedjs.build_pagedjs import compile_pagedjs


def parse_bleed_to_mm(bleed_str: str) -> float:
    """Parses bleed string (e.g. '3mm', '3.0mm', '3') to float in millimeters."""
    if not bleed_str:
        return 3.0
    cleaned = re.sub(r'[^\d.]', '', str(bleed_str))
    try:
        if not cleaned:
            if str(bleed_str).strip():
                sys.stderr.write(f"[WARNING] Invalid bleed value '{bleed_str}', defaulting to 3.0mm\n")
            return 3.0
        return float(cleaned)
    except ValueError:
        sys.stderr.write(f"[WARNING] Invalid bleed value '{bleed_str}', defaulting to 3.0mm\n")
        return 3.0


def resolve_engine_for_input(input_path: str, requested_engine: str = "auto") -> str:
    """
    Resolves the compilation engine based on requested setting and file extension.
    """
    if requested_engine in ("typst", "pagedjs", "both"):
        return requested_engine

    ext = os.path.splitext(input_path)[1].lower()
    if ext == ".typ":
        return "typst"
    elif ext in (".html", ".htm"):
        return "pagedjs"
    elif ext == ".json":
        # Check manifest contents if JSON
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "engine" in data and data["engine"] in ("typst", "pagedjs", "both"):
                return data["engine"]
            if "source" in data:
                src_ext = os.path.splitext(data["source"])[1].lower()
                if src_ext == ".typ":
                    return "typst"
                elif src_ext in (".html", ".htm"):
                    return "pagedjs"
        except Exception:
            pass

    return "typst"


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
    """
    Unified dual-engine compilation dispatcher.

    Args:
        input_path: Path to input document (.typ, .html, or manifest.json).
        output_path: Destination path for compiled PDF.
        engine: 'typst', 'pagedjs', 'both', or 'auto'.
        bleed: Bleed specification (default: '3mm').
        profile: Color profile identifier (default: 'FOGRA51').
        benchmark: If True, tracks detailed execution telemetry.
        timeout_sec: Timeout in seconds for compilation subprocess.

    Returns:
        Compilation status dictionary.
    """
    total_start = time.perf_counter()
    bleed_mm = parse_bleed_to_mm(bleed)

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if os.path.getsize(input_path) == 0:
        raise ValueError(f"Input source file is empty (0 bytes): {input_path}")

    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        src_peek = f.read()
    if not src_peek.strip():
        raise ValueError(f"Input source file is empty: {input_path}")

    if engine not in ("typst", "pagedjs", "both", "auto"):
        raise ValueError(f"Unsupported compilation engine: {engine}")

    ext = os.path.splitext(input_path)[1].lower()
    if engine == "typst" and ext in (".html", ".htm"):
        raise ValueError(f"Mismatched engine: cannot compile HTML input file '{input_path}' with engine 'typst'")
    if engine == "pagedjs" and ext == ".typ":
        raise ValueError(f"Mismatched engine: cannot compile Typst input file '{input_path}' with engine 'pagedjs'")

    resolved_engine = resolve_engine_for_input(input_path, engine)

    if not output_path:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}.pdf"

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    if resolved_engine == "typst":
        res = compile_typst(
            input_path=input_path,
            output_path=output_path,
            timeout_sec=timeout_sec,
            bleed_mm=bleed_mm,
            profile=profile,
            **kwargs
        )
        total_duration = time.perf_counter() - total_start
        res["total_duration_sec"] = round(total_duration, 4)
        if benchmark:
            res["benchmark"] = {
                "engine_duration_sec": res["duration_sec"],
                "total_duration_sec": res["total_duration_sec"],
                "output_size_bytes": os.path.getsize(output_path),
                "pages_per_second": round(res["page_count"] / max(res["duration_sec"], 0.001), 2)
            }
        return res

    elif resolved_engine == "pagedjs":
        res = compile_pagedjs(
            input_html=input_path,
            output_pdf=output_path,
            timeout_sec=timeout_sec,
            bleed_mm=bleed_mm,
            profile=profile,
            **kwargs
        )
        total_duration = time.perf_counter() - total_start
        res["total_duration_sec"] = round(total_duration, 4)
        if benchmark:
            res["benchmark"] = {
                "engine_duration_sec": res["duration_sec"],
                "total_duration_sec": res["total_duration_sec"],
                "output_size_bytes": os.path.getsize(output_path),
                "pages_per_second": round(res["page_count"] / max(res["duration_sec"], 0.001), 2)
            }
        return res

    elif resolved_engine == "both":
        # Dual-engine compilation
        base_out, ext_out = os.path.splitext(output_path)
        out_typ = f"{base_out}_typst{ext_out}"
        out_paged = f"{base_out}_pagedjs{ext_out}"

        input_dir = os.path.dirname(os.path.abspath(input_path))
        base_in, ext_in = os.path.splitext(os.path.basename(input_path))

        typst_src = input_path if ext_in == ".typ" else os.path.join(input_dir, f"{base_in}.typ")
        paged_src = input_path if ext_in in (".html", ".htm") else os.path.join(input_dir, f"{base_in}.html")

        # Fallback to template files if corresponding files don't exist
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if not os.path.isfile(typst_src):
            typst_src = os.path.join(repo_root, "engine", "typst", "template.typ")
        if not os.path.isfile(paged_src):
            paged_src = os.path.join(repo_root, "engine", "pagedjs", "template.html")

        res_typ = compile_typst(typst_src, out_typ, timeout_sec=timeout_sec, bleed_mm=bleed_mm, **kwargs)
        res_paged = compile_pagedjs(paged_src, out_paged, timeout_sec=timeout_sec, bleed_mm=bleed_mm, **kwargs)

        total_duration = time.perf_counter() - total_start
        combined_res = {
            "success": res_typ["success"] and res_paged["success"],
            "engine": "both",
            "output_path": output_path,
            "outputs": {
                "typst": res_typ,
                "pagedjs": res_paged
            },
            "page_count": max(res_typ.get("page_count", 0), res_paged.get("page_count", 0)),
            "duration_sec": round(total_duration, 4),
            "total_duration_sec": round(total_duration, 4)
        }
        if benchmark:
            combined_res["benchmark"] = {
                "typst_duration_sec": res_typ["duration_sec"],
                "pagedjs_duration_sec": res_paged["duration_sec"],
                "total_duration_sec": combined_res["total_duration_sec"]
            }
        return combined_res

    else:
        raise ValueError(f"Unsupported compilation engine: {resolved_engine}")


def main():
    parser = argparse.ArgumentParser(
        description="Editorial Studio Unified Dual-Engine Compilation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-i", "--input", help="Path to input source file (.typ, .html, or manifest.json)")
    parser.add_argument("-m", "--manifest", help="Alias for input manifest file")
    parser.add_argument("-o", "--output", help="Path for output PDF")
    parser.add_argument(
        "-e", "--engine",
        choices=["typst", "pagedjs", "both", "auto"],
        default="auto",
        help="Target compilation engine (default: auto)"
    )
    parser.add_argument("--bleed", default="3mm", help="Bleed allowance (default: 3mm)")
    parser.add_argument("--profile", default="FOGRA51", help="Target print ICC color profile (default: FOGRA51)")
    parser.add_argument("--benchmark", action="store_true", help="Report detailed compilation benchmarking metrics")
    parser.add_argument("-t", "--timeout", type=float, default=30.0, help="Compilation timeout in seconds")

    args = parser.parse_args()

    input_file = args.input or args.manifest
    if not input_file:
        parser.error("Either --input or --manifest must be specified.")

    output_file = args.output
    if not output_file:
        base, _ = os.path.splitext(input_file)
        output_file = f"{base}.pdf"

    try:
        result = compile_document(
            input_path=input_file,
            output_path=output_file,
            engine=args.engine,
            bleed=args.bleed,
            profile=args.profile,
            benchmark=args.benchmark,
            timeout_sec=args.timeout
        )

        print("============================================================")
        print("EDITORIAL-STUDIO UNIFIED COMPILATION COMPLETED")
        print("============================================================")
        print(f"Engine:      {result['engine']}")
        print(f"Input:       {input_file}")
        print(f"Output:      {result['output_path']}")
        print(f"Pages:       {result['page_count']}")
        print(f"Duration:    {result['duration_sec']}s")
        print(f"Status:      SUCCESS")
        if args.benchmark and "benchmark" in result:
            bm = result["benchmark"]
            print("------------------------------------------------------------")
            print("BENCHMARK METRICS:")
            for k, v in bm.items():
                print(f"  {k}: {v}")
        print("============================================================")
        sys.exit(0)
    except Exception as exc:
        print(f"[ERROR] Compilation failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
