import os
import platform
import subprocess

import screen_brightness_control as sbc

from comtypes import CoInitialize, CoUninitialize
from pycaw.pycaw import AudioUtilities


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

    try:
        os.startfile(uri)

        return {"success": True, "message": f"Opened {setting} settings."}

    except Exception as e:
        return {"success": False, "message": str(e)}


def lock_pc():
    try:
        subprocess.Popen(["rundll32.exe", "user32.dll,LockWorkStation"])

        return {"success": True, "message": "Computer locked."}

    except Exception as e:
        return {"success": False, "message": str(e)}


def system_info():
    try:
        return {
            "success": True,
            "data": {
                "os": platform.system(),
                "version": platform.version(),
                "machine": platform.machine(),
                "username": os.getlogin(),
            },
        }

    except Exception as e:
        return {"success": False, "message": str(e)}


def get_audio_interface():
    device = AudioUtilities.GetSpeakers()
    return device.EndpointVolume


def set_volume(level: int):
    CoInitialize()

    try:
        level = int(level)

        if not 0 <= level <= 100:
            return {"success": False, "message": "Volume must be between 0 and 100."}

        volume = get_audio_interface()

        # Unmute automatically
        volume.SetMute(0, None)

        # Convert percentage to Windows scalar
        scalar = level / 100.0

        volume.SetMasterVolumeLevelScalar(scalar, None)

        actual_scalar = volume.GetMasterVolumeLevelScalar()

        actual = round(actual_scalar * 100)

        print(f"[AUDIO] Requested volume: {level}%")

        print(f"[AUDIO] Actual volume: {actual}%")

        return {
            "success": True,
            "message": f"Volume set to {actual}%.",
            "requested": level,
            "actual": actual,
        }

    except Exception as e:
        print(f"[AUDIO ERROR] {repr(e)}")

        return {"success": False, "message": str(e)}

    finally:
        CoUninitialize()


def get_volume():
    CoInitialize()

    try:
        volume = get_audio_interface()

        level = round(volume.GetMasterVolumeLevelScalar() * 100)

        muted = bool(volume.GetMute())

        return {"success": True, "volume": level, "muted": muted}

    except Exception as e:
        return {"success": False, "message": str(e)}

    finally:
        CoUninitialize()


def mute_audio():
    CoInitialize()

    try:
        volume = get_audio_interface()

        volume.SetMute(1, None)

        muted = bool(volume.GetMute())

        return {"success": True, "message": "Audio muted.", "muted": muted}

    except Exception as e:
        return {"success": False, "message": str(e)}

    finally:
        CoUninitialize()


def unmute_audio():
    CoInitialize()

    try:
        volume = get_audio_interface()

        volume.SetMute(0, None)

        muted = bool(volume.GetMute())

        return {"success": True, "message": "Audio unmuted.", "muted": muted}

    except Exception as e:
        return {"success": False, "message": str(e)}

    finally:
        CoUninitialize()


def set_brightness(level: int):
    try:
        level = int(level)

        if not 0 <= level <= 100:
            return {
                "success": False,
                "message": "Brightness must be between 0 and 100.",
            }

        sbc.set_brightness(level)

        actual = sbc.get_brightness()

        return {
            "success": True,
            "message": f"Brightness set to {level}%.",
            "requested": level,
            "actual": actual,
        }

    except Exception as e:
        return {"success": False, "message": str(e)}
