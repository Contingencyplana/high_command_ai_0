"""Template rendering utilities for Forge."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
except ModuleNotFoundError as exc:  # pragma: no cover - handled gracefully at runtime
    raise ImportError(
        "Forge requires the 'jinja2' package for template rendering. Install it with 'pip install jinja2'."
    ) from exc

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = ROOT / "template" / "forge"
_ENVIRONMENT: Environment | None = None


class TemplateEngineError(RuntimeError):
    """Raised when the template engine encounters an unrecoverable error."""


def _load_filters() -> Dict[str, Any]:
    filters_path = TEMPLATE_ROOT / "macros" / "filters.py"
    if not filters_path.exists():
        return {}
    module_name = "forge_template_filters"
    spec = importlib.util.spec_from_file_location(module_name, filters_path)
    if spec is None or spec.loader is None:
        raise TemplateEngineError(f"Unable to load filters module at {filters_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return {
        name: getattr(module, name)
        for name in dir(module)
        if not name.startswith("_") and callable(getattr(module, name))
    }


def get_environment() -> Environment:
    global _ENVIRONMENT
    if _ENVIRONMENT is None:
        if not TEMPLATE_ROOT.exists():
            raise TemplateEngineError(f"Template root missing at {TEMPLATE_ROOT}")
        env = Environment(  # nosec - templates are trusted project assets
            loader=FileSystemLoader(str(TEMPLATE_ROOT)),
            autoescape=False,
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        env.filters.update(_load_filters())
        _ENVIRONMENT = env
    return _ENVIRONMENT


def render_template(relative_path: str, context: Dict[str, Any]) -> str:
    """Render the given template with context, raising TemplateEngineError on failure."""
    environment = get_environment()
    try:
        template = environment.get_template(relative_path)
    except Exception as exc:  # pragma: no cover - dependent on template availability
        raise TemplateEngineError(f"Failed to load template '{relative_path}': {exc}") from exc
    try:
        rendered = template.render(**context)
    except Exception as exc:  # pragma: no cover - dependent on template content
        raise TemplateEngineError(f"Failed to render template '{relative_path}': {exc}") from exc
    # Ensure trailing newline for git-friendly diffs.
    if not rendered.endswith("\n"):
        rendered += "\n"
    return rendered
