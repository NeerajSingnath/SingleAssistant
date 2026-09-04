import os
import subprocess
from pathlib import Path

START_MENU_PATHS = [
    Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs",
    Path(os.environ["PROGRAMDATA"]) / "Microsoft/Windows/Start Menu/Programs",
]


def discover_apps():
    apps = {}

    for base_path in START_MENU_PATHS:
        if not base_path.exists():
            continue

        for item in base_path.rglob("*.lnk"):
            name = item.stem.lower().strip()

            apps[name] = str(item)

    return apps


def find_app(app_name: str):
    app_name = app_name.lower().strip()

    apps = discover_apps()

    # Exact match
    if app_name in apps:
        return apps[app_name]

    # Partial match
    for name, path in apps.items():
        if app_name in name:
            return path

    return None


def open_dynamic_app(app_name: str):
    try:
        app_path = find_app(app_name)

        if not app_path:
            return {
                "success": False,
                "message": f"Could not find installed app: {app_name}",
            }

        os.startfile(app_path)

        return {"success": True, "message": f"Opened {app_name}.", "path": app_path}

    except Exception as e:
        return {"success": False, "message": str(e)}
