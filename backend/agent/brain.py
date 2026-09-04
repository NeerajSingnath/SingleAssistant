from agent.tool_registry import execute_tool


def process_command(command: str):

    text = command.lower().strip()

    # OPEN APPLICATION

    if text.startswith("open "):

        app = text.replace("open ", "", 1)

        settings = [
            "bluetooth",
            "wifi",
            "display",
            "sound",
            "notifications",
            "windows update",
            "privacy",
        ]

        if app.endswith(" settings"):
            setting = app.replace(" settings", "")

            return execute_tool("open_settings", {"setting": setting})

        if app in settings:
            return execute_tool("open_settings", {"setting": app})

        return execute_tool("open_app", {"app_name": app})

    # CLOSE APPLICATION

    if text.startswith("close "):

        app = text.replace("close ", "", 1)

        return execute_tool("close_app", {"app_name": app})

    # LOCK PC

    if text in ["lock pc", "lock computer", "lock my computer"]:

        return execute_tool("lock_pc", {})

    # SYSTEM INFO

    if text in ["system info", "computer info", "pc info"]:

        return execute_tool("system_info", {})

    return {"success": False, "message": "I don't understand that command yet."}
