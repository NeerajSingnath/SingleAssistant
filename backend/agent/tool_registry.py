from tools.apps import open_app, close_app, open_chrome

from tools.system import (
    open_settings,
    lock_pc,
    system_info,
    set_volume,
    get_volume,
    mute_audio,
    unmute_audio,
    set_brightness,
)

from tools.windows_apps import (
    open_dynamic_app,
)

from tools.files import (
    open_folder,
    open_path,
)

from tools.media import (
    take_screenshot,
    play_pause_media,
    next_track,
    previous_track,
    volume_up,
    volume_down,
)

TOOLS = {
    "open_app": open_app,
    "close_app": close_app,
    "open_chrome": open_chrome,
    "open_dynamic_app": open_dynamic_app,
    "open_folder": open_folder,
    "open_path": open_path,
    "open_settings": open_settings,
    "lock_pc": lock_pc,
    "system_info": system_info,
    "set_volume": set_volume,
    "get_volume": get_volume,
    "mute_audio": mute_audio,
    "unmute_audio": unmute_audio,
    "set_brightness": set_brightness,
    "take_screenshot": take_screenshot,
    "play_pause_media": play_pause_media,
    "next_track": next_track,
    "previous_track": previous_track,
    "volume_up": volume_up,
    "volume_down": volume_down,
}


def execute_tool(tool_name: str, arguments: dict):
    tool = TOOLS.get(tool_name)

    if not tool:
        return {"success": False, "message": f"Unknown tool: {tool_name}"}

    try:
        return tool(**arguments)

    except Exception as e:
        return {"success": False, "message": str(e)}
