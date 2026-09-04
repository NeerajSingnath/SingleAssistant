import json
import ollama

from agent.tool_registry import execute_tool

SYSTEM_PROMPT = """
You are the planning brain of a Windows desktop assistant.

Your job is to convert the user's request into a tool call.

Available tools:

1. open_app
arguments:
{
    "app_name": string
}

Supported apps:
notepad
calculator
paint
explorer


2. close_app
arguments:
{
    "app_name": string
}

Supported apps:
chrome
notepad
paint
calculator


3. open_chrome
arguments:
{
    "profile": "main" | "second" | "college" | "backup",
    "url": string | null
}

Chrome profile mappings:
main = user's primary personal Chrome
second = user's second Chrome profile
college = user's college Chrome
backup = user's backup Chrome


4. open_settings
arguments:
{
    "setting": string
}

Supported settings:
bluetooth
wifi
display
sound
notifications
apps
windows update
privacy


5. lock_pc
arguments:
{}


6. system_info
arguments:
{}


Return ONLY valid JSON.

Format:

{
    "tool": "tool_name",
    "arguments": {}
}

Examples:

User: Open Chrome
{
    "tool": "open_chrome",
    "arguments": {
        "profile": "main",
        "url": null
    }
}

User: Open my college Chrome
{
    "tool": "open_chrome",
    "arguments": {
        "profile": "college",
        "url": null
    }
}

User: Open Classroom in my college account
{
    "tool": "open_chrome",
    "arguments": {
        "profile": "college",
        "url": "https://classroom.google.com"
    }
}

User: Open Bluetooth settings
{
    "tool": "open_settings",
    "arguments": {
        "setting": "bluetooth"
    }
}

User: Close Chrome
{
    "tool": "close_app",
    "arguments": {
        "app_name": "chrome"
    }
}

Do not invent tools.
Do not execute commands yourself.
"""


def get_tool_call(command: str):

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": command},
        ],
        format="json",
    )

    content = response["message"]["content"]

    try:
        data = json.loads(content)

        return data

    except json.JSONDecodeError:

        return {"tool": None, "arguments": {}, "error": "Model returned invalid JSON"}


def process_command(command: str):

    tool_call = get_tool_call(command)

    tool_name = tool_call.get("tool")
    arguments = tool_call.get("arguments", {})

    if not tool_name:
        return {
            "success": False,
            "message": tool_call.get(
                "error", "Unable to determine the requested action."
            ),
        }

    result = execute_tool(tool_name, arguments)

    return {"tool": tool_name, "arguments": arguments, "result": result}
