import subprocess
import psutil

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
APP_PATHS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "settings": "ms-settings:",
    "explorer": "explorer.exe",
}

CHROME_PROFILES = {
    "main": "Default",
    "second": "Profile 4",
    "college": "Profile 12",
    "backup": "Profile 6",
}


def open_chrome(profile: str = "main", url: str | None = None):

    profile = profile.lower().strip()

    profile_directory = CHROME_PROFILES.get(profile)

    if not profile_directory:
        return {"success": False, "message": f"Unknown Chrome profile: {profile}"}

    command = [CHROME_PATH, f"--profile-directory={profile_directory}"]

    if url:
        command.append(url)

    subprocess.Popen(command)

    return {"success": True, "message": f"Opened Chrome using the {profile} profile."}


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
