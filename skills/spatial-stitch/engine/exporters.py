"""
exporters.py - Multi-format export: SVG, HTML5 Print Sheets, InDesign JSON
"""

from pathlib import Path
from .models import SpreadInstance


class DocumentExporter:
    @staticmethod
    def export_svg(spread: SpreadInstance, out_path: Path) -> Path:
        out_path = Path(out_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(spread.svg_content, encoding="utf-8")
        return out_path

    @staticmethod
    def export_html(spread: SpreadInstance, out_path: Path) -> Path:
        out_path = Path(out_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        full_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{spread.title}</title>
    <style>
        @page {{ size: landscape; margin: 0; }}
        body {{ margin: 0; padding: 0; background: #E5E5E5; display: flex; justify-content: center; align-items: center; min-height: 100vh; font-family: Inter, sans-serif; }}
        .spread-container {{ width: {spread.width}px; height: {spread.height}px; box-shadow: 0 20px 50px rgba(0,0,0,0.15); }}
        svg {{ width: 100%; height: 100%; display: block; }}
    </style>
</head>
<body>
    <div class="spread-container">
        {spread.svg_content}
    </div>
</body>
</html>"""
        out_path.write_text(full_doc, encoding="utf-8")
        return out_path
