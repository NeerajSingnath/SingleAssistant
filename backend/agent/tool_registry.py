from tools.apps import open_app, close_app, open_chrome
from tools.system import open_settings, lock_pc, system_info

TOOLS = {
    "open_app": open_app,
    "close_app": close_app,
    "open_chrome": open_chrome,
    "open_settings": open_settings,
    "lock_pc": lock_pc,
    "system_info": system_info,
}


def execute_tool(tool_name: str, arguments: dict):
    tool = TOOLS.get(tool_name)

    if not tool:
        return {"success": False, "message": f"Unknown tool: {tool_name}"}

    try:
        return tool(**arguments)

    except Exception as e:
        return {"success": False, "message": str(e)}
