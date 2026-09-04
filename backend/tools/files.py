import os
from pathlib import Path

HOME = Path.home()


COMMON_FOLDERS = {
    "desktop": HOME / "Desktop",
    "downloads": HOME / "Downloads",
    "documents": HOME / "Documents",
    "pictures": HOME / "Pictures",
    "videos": HOME / "Videos",
    "music": HOME / "Music",
}


def open_folder(folder: str):
    try:
        folder = folder.lower().strip()

        path = COMMON_FOLDERS.get(folder)

        if not path:
            return {"success": False, "message": f"Unknown folder: {folder}"}

        if not path.exists():
            return {"success": False, "message": f"Folder does not exist: {path}"}

        os.startfile(path)

        return {
            "success": True,
            "message": f"Opened {folder} folder.",
            "path": str(path),
        }

    except Exception as e:
        return {"success": False, "message": str(e)}


def open_path(path: str):
    try:
        target = Path(path).expanduser()

        if not target.exists():
            return {"success": False, "message": f"Path not found: {path}"}

        os.startfile(target)

        return {"success": True, "message": f"Opened {target}.", "path": str(target)}

    except Exception as e:
        return {"success": False, "message": str(e)}
