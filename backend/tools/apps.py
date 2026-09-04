import subprocess
import psutil

APP_PATHS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "settings": "ms-settings:",
    "explorer": "explorer.exe",
}


def open_app(app_name: str):
    app_name = app_name.lower().strip()

    if app_name not in APP_PATHS:
        return {
            "success": False,
            "message": f"I don't know how to open {app_name} yet.",
        }

    try:
        path = APP_PATHS[app_name]

        if path.startswith("ms-settings:"):
            subprocess.Popen(["cmd", "/c", "start", "", path], shell=True)
        else:
            subprocess.Popen(path)

        return {"success": True, "message": f"Opened {app_name}."}

    except Exception as e:
        return {"success": False, "message": str(e)}


def close_app(app_name: str):
    app_name = app_name.lower().strip()

    process_names = {
        "chrome": "chrome.exe",
        "notepad": "notepad.exe",
        "paint": "mspaint.exe",
        "calculator": "CalculatorApp.exe",
    }

    if app_name not in process_names:
        return {
            "success": False,
            "message": f"I don't know how to close {app_name} yet.",
        }

    target = process_names[app_name]

    killed = 0

    for process in psutil.process_iter(["name"]):
        try:
            if process.info["name"] == target:
                process.terminate()
                killed += 1

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if killed == 0:
        return {"success": False, "message": f"{app_name} doesn't seem to be running."}

    return {"success": True, "message": f"Closed {app_name}."}
