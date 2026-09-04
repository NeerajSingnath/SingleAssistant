from pathlib import Path
from datetime import datetime

import pyautogui

SCREENSHOT_DIR = Path.home() / "Pictures" / "Mohdihhji Screenshots"


def take_screenshot():
    try:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        path = SCREENSHOT_DIR / f"screenshot_{timestamp}.png"

        screenshot = pyautogui.screenshot()
        screenshot.save(path)

        return {
            "success": True,
            "message": "Screenshot captured.",
            "path": str(path),
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }


def play_pause_media():
    try:
        pyautogui.press("playpause")

        return {"success": True, "message": "Toggled play/pause."}

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }


def next_track():
    try:
        pyautogui.press("nexttrack")

        return {"success": True, "message": "Skipped to next track."}

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }


def previous_track():
    try:
        pyautogui.press("prevtrack")

        return {"success": True, "message": "Went to previous track."}

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }


def volume_up(steps: int = 1):
    try:
        steps = max(1, min(int(steps), 20))

        for _ in range(steps):
            pyautogui.press("volumeup")

        return {"success": True, "message": f"Increased volume by {steps} step(s)."}

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }


def volume_down(steps: int = 1):
    try:
        steps = max(1, min(int(steps), 20))

        for _ in range(steps):
            pyautogui.press("volumedown")

        return {"success": True, "message": f"Decreased volume by {steps} step(s)."}

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }
