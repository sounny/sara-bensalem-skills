"""
project_manager.py - Manages Project Lifecycle & Local Spread Persistence
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from .models import PortfolioProject, SpreadInstance, CanvasFormat, ProjectPassport


class ProjectManager:
    def __init__(self, storage_dir: Path = None):
        self.storage_dir = storage_dir or (Path("g:/My Drive/Portfolios/spatial-stitch/data")).resolve()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.projects_file = self.storage_dir / "projects.json"
        self.spreads_dir = self.storage_dir / "spreads"
        self.spreads_dir.mkdir(parents=True, exist_ok=True)
        self.projects: Dict[str, PortfolioProject] = self._load_projects()

    def _load_projects(self) -> Dict[str, PortfolioProject]:
        if self.projects_file.exists():
            try:
                data = json.loads(self.projects_file.read_text(encoding="utf-8"))
                return {k: PortfolioProject(**v) for k, v in data.items()}
            except Exception:
                pass
        return {}

    def _save_projects(self):
        data = {k: v.model_dump() for k, v in self.projects.items()}
        self.projects_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def create_project(self, name: str, description: str = "", format: CanvasFormat = CanvasFormat.LANDSCAPE_16_9, passport: ProjectPassport = None) -> PortfolioProject:
        passport = passport or ProjectPassport(title=name)
        proj = PortfolioProject(name=name, description=description, canvas_format=format, passport=passport)
        self.projects[proj.id] = proj
        self._save_projects()
        return proj

    def get_project(self, project_id: str) -> Optional[PortfolioProject]:
        return self.projects.get(project_id)

    def list_projects(self) -> List[PortfolioProject]:
        return list(self.projects.values())

    def save_spread(self, spread: SpreadInstance):
        proj = self.projects.get(spread.project_id)
        if proj and spread.id not in proj.spread_ids:
            proj.spread_ids.append(spread.id)
            self._save_projects()

        spread_file = self.spreads_dir / f"{spread.id}.json"
        spread_file.write_text(json.dumps(spread.model_dump(), indent=2), encoding="utf-8")

    def get_spread(self, spread_id: str) -> Optional[SpreadInstance]:
        spread_file = self.spreads_dir / f"{spread_id}.json"
        if spread_file.exists():
            data = json.loads(spread_file.read_text(encoding="utf-8"))
            return SpreadInstance(**data)
        return None
