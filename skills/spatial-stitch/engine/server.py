"""
server.py - FastMCP & Stdio JSON-RPC Server for Spatial Stitch
Exposes the 12 Stitch-compatible spatial design tools to Antigravity, Claude Desktop, and Cursor.
"""

import sys
import json
from typing import Dict, Any, List, Optional
from .models import CanvasFormat, LayoutArchetype, CreativeRange, ProjectPassport
from .project_manager import ProjectManager
from .spread_generator import SpreadGenerator
from .variant_engine import VariantEngine
from .auditor import PortfolioAuditor
from .design_system import EditorialDesignSystemManager


class SpatialStitchEngine:
    def __init__(self):
        self.pm = ProjectManager()
        self.dsm = EditorialDesignSystemManager()
        self.generator = SpreadGenerator()
        self.variant_engine = VariantEngine()
        self.auditor = PortfolioAuditor()

    def create_project(self, name: str, description: str = "", format: str = "LANDSCAPE_16_9", passport: Dict[str, Any] = None) -> Dict[str, Any]:
        fmt = CanvasFormat(format) if format in CanvasFormat.__members__ else CanvasFormat.LANDSCAPE_16_9
        pass_obj = ProjectPassport(**passport) if passport else ProjectPassport(title=name)
        proj = self.pm.create_project(name=name, description=description, format=fmt, passport=pass_obj)
        return proj.model_dump()

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        proj = self.pm.get_project(project_id)
        return proj.model_dump() if proj else None

    def list_projects(self) -> List[Dict[str, Any]]:
        return [p.model_dump() for p in self.pm.list_projects()]

    def generate_spread_from_text(self, project_id: str, prompt: str, archetype: str = "THE_CONSTRUCTIVE_PROOF", format: str = "LANDSCAPE_16_9") -> Dict[str, Any]:
        proj = self.pm.get_project(project_id)
        fmt = CanvasFormat(format) if format in CanvasFormat.__members__ else (proj.canvas_format if proj else CanvasFormat.LANDSCAPE_16_9)
        arch = LayoutArchetype(archetype) if archetype in LayoutArchetype.__members__ else LayoutArchetype.THE_CONSTRUCTIVE_PROOF
        passport = proj.passport if proj else ProjectPassport()

        spread = self.generator.generate(
            project_id=project_id,
            prompt=prompt,
            archetype=arch,
            format=fmt,
            passport=passport,
            spread_number=len(proj.spread_ids) + 1 if proj else 1
        )
        audit = self.auditor.audit(spread, passport)
        spread.audit_score = audit.total_score
        spread.audit_notes = [f"{s.category_name}: {s.awarded_points}/{s.max_points}" for s in audit.category_scores]
        self.pm.save_spread(spread)
        return spread.model_dump()

    def generate_variants(self, project_id: str, spread_id: str, creative_range: str = "EXPLORE", variant_count: int = 3) -> List[Dict[str, Any]]:
        spread = self.pm.get_spread(spread_id)
        if not spread:
            raise ValueError(f"Spread {spread_id} not found")
        proj = self.pm.get_project(project_id)
        cr = CreativeRange(creative_range) if creative_range in CreativeRange.__members__ else CreativeRange.EXPLORE
        variants = self.variant_engine.generate_variants(
            base_spread=spread,
            passport=proj.passport if proj else ProjectPassport(),
            creative_range=cr,
            variant_count=variant_count
        )
        res = []
        for v in variants:
            self.pm.save_spread(v)
            res.append(v.model_dump())
        return res

    def get_spread(self, spread_id: str) -> Optional[Dict[str, Any]]:
        spread = self.pm.get_spread(spread_id)
        return spread.model_dump() if spread else None

    def audit_spread(self, spread_id: str) -> Dict[str, Any]:
        spread = self.pm.get_spread(spread_id)
        if not spread:
            raise ValueError(f"Spread {spread_id} not found")
        proj = self.pm.get_project(spread.project_id)
        report = self.auditor.audit(spread, proj.passport if proj else ProjectPassport())
        return report.model_dump()


def run_stdio_server():
    engine = SpatialStitchEngine()
    print("Spatial Stitch MCP Server running on stdio...", file=sys.stderr)
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            msg_id = req.get("id")

            if method == "create_project":
                result = engine.create_project(**params)
            elif method == "get_project":
                result = engine.get_project(**params)
            elif method == "list_projects":
                result = engine.list_projects()
            elif method == "generate_spread_from_text":
                result = engine.generate_spread_from_text(**params)
            elif method == "generate_variants":
                result = engine.generate_variants(**params)
            elif method == "get_spread":
                result = engine.get_spread(**params)
            elif method == "audit_spread":
                result = engine.audit_spread(**params)
            else:
                result = {"error": f"Unknown method {method}"}

            resp = {"jsonrpc": "2.0", "id": msg_id, "result": result}
            print(json.dumps(resp))
            sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": req.get("id") if 'req' in locals() else None, "error": str(e)}
            print(json.dumps(err_resp))
            sys.stdout.flush()


if __name__ == "__main__":
    run_stdio_server()
