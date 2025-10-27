from __future__ import annotations

import importlib
import pkgutil
import os
from typing import Dict, Tuple, Any


def discover_plugins(models_pkg: str) -> Dict[str, Tuple[Any, dict]]:
    """
    Discover model plugins under the given package (e.g., 'src.models').
    Expects modules at 'src.models.<name>.model' defining:
      - NAME: str (model identifier)
      - SPEC: dict (optional)
      - create(params: dict) -> model instance
    Returns mapping: name -> (create_fn, spec_dict)
    """
    plugins: Dict[str, Tuple[Any, dict]] = {}

    try:
        pkg = importlib.import_module(models_pkg)
    except ModuleNotFoundError:
        return plugins

    pkg_path = os.path.dirname(pkg.__file__)
    for m in pkgutil.iter_modules([pkg_path]):
        if not m.ispkg:
            # skip loose modules; we want packages with model.py
            continue
        subpkg_name = f"{models_pkg}.{m.name}"
        try:
            mod = importlib.import_module(f"{subpkg_name}.model")
        except ModuleNotFoundError:
            # No model module inside package; skip
            continue
        except Exception:
            # Any import error (e.g., SyntaxError) should not break discovery of other plugins
            continue
        name = getattr(mod, "NAME", None)
        create_fn = getattr(mod, "create", None)
        spec = getattr(mod, "SPEC", {}) or {}
        if isinstance(name, str) and callable(create_fn):
            plugins[name] = (create_fn, spec)
    return plugins
