import subprocess
import platform
import os


def open_settings(setting: str):
    setting = setting.lower().strip()

    settings_map = {
        "bluetooth": "ms-settings:bluetooth",
        "wifi": "ms-settings:network-wifi",
        "display": "ms-settings:display",
        "sound": "ms-settings:sound",
        "notifications": "ms-settings:notifications",
        "apps": "ms-settings:appsfeatures",
        "windows update": "ms-settings:windowsupdate",
        "privacy": "ms-settings:privacy",
    }

    uri = settings_map.get(setting)

    if not uri:
        return {"success": False, "message": f"Unknown setting: {setting}"}

    subprocess.Popen(["cmd", "/c", "start", "", uri], shell=True)

    return {"success": True, "message": f"Opened {setting} settings."}


def lock_pc():
    subprocess.Popen(["rundll32.exe", "user32.dll,LockWorkStation"])

    return {"success": True, "message": "Computer locked."}


def system_info():
    return {
        "success": True,
        "data": {
            "os": platform.system(),
            "version": platform.version(),
            "machine": platform.machine(),
            "username": os.getlogin(),
        },
    }
