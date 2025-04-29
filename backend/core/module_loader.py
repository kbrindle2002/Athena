import importlib
import pkgutil
from pathlib import Path
from typing import List

MODULES_PATH = Path(__file__).resolve().parents[1] / "modules"

def load_enabled_modules() -> List:
    routers = []
    if not MODULES_PATH.exists():
        return routers
    for module in pkgutil.iter_modules([str(MODULES_PATH)]):
        if module.ispkg:
            mod = importlib.import_module(f"modules.{module.name}.routes")
            routers.append(getattr(mod, "router"))
    return routers
