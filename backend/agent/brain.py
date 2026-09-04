from agent.tool_registry import execute_tool


def process_command(command: str):

    text = command.lower().strip()

    # -------------------------
    # CHROME
    # -------------------------

    if text == "open chrome":
        return execute_tool("open_chrome", {"profile": "main"})

    if text == "open main chrome":
        return execute_tool("open_chrome", {"profile": "main"})

    if text == "open second chrome":
        return execute_tool("open_chrome", {"profile": "second"})

    if text == "open college chrome":
        return execute_tool("open_chrome", {"profile": "college"})

    if text == "open backup chrome":
        return execute_tool("open_chrome", {"profile": "backup"})

    # -------------------------
    # SPECIAL CHROME URL
    # -------------------------

    if text == "open classroom":
        return execute_tool(
            "open_chrome", {"profile": "college", "url": "https://classroom.google.com"}
        )

    # -------------------------
    # OPEN
    # -------------------------

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

    # -------------------------
    # CLOSE
    # -------------------------

    if text.startswith("close "):

        app = text.replace("close ", "", 1)

        return execute_tool("close_app", {"app_name": app})

    return {"success": False, "message": "I don't understand that command yet."}
