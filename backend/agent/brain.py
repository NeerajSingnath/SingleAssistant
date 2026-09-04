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

7. set_volume
arguments:
{
    "level": integer
}

Sets Windows volume from 0 to 100.


8. get_volume
arguments:
{}

Returns current system volume and mute state.


9. mute_audio
arguments:
{}


10. unmute_audio
arguments:
{}


11. set_brightness
arguments:
{
    "level": integer
}

Sets display brightness from 0 to 100.


Return ONLY valid JSON.

Always return an object containing an "actions" array.

Format:

{
    "actions": [
        {
            "tool": "tool_name",
            "arguments": {}
        }
    ]
}

User: Set volume to 30 percent

{
    "actions": [
        {
            "tool": "set_volume",
            "arguments": {
                "level": 30
            }
        }
    ]
}


User: Mute the computer

{
    "actions": [
        {
            "tool": "mute_audio",
            "arguments": {}
        }
    ]
}

Examples:
User: Set volume to 30 percent

{
    "actions": [
        {
            "tool": "set_volume",
            "arguments": {
                "level": 30
            }
        }
    ]
}


User: Mute the computer

{
    "actions": [
        {
            "tool": "mute_audio",
            "arguments": {}
        }
    ]
}


User: Set brightness to 70%

{
    "actions": [
        {
            "tool": "set_brightness",
            "arguments": {
                "level": 70
            }
        }
    ]
}

You MUST include every explicitly requested action.

If the user asks for N distinct actions,
the actions array must contain N corresponding actions.

Do not omit an action because another action seems more important.

Example:

User:
Open Chrome, Notepad and Bluetooth settings.

Correct:
{
  "actions": [
    {
      "tool": "open_chrome",
      "arguments": {
        "profile": "main",
        "url": null
      }
    },
    {
      "tool": "open_app",
      "arguments": {
        "app_name": "notepad"
      }
    },
    {
      "tool": "open_settings",
      "arguments": {
        "setting": "bluetooth"
      }
    }
  ]
}

Never invent tools.
Never return shell commands.
Only use tools explicitly available to you.
"""


def get_plan(command: str):

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

        if "actions" not in data:
            return {"actions": [], "error": "Model did not return an actions list."}

        return data

    except json.JSONDecodeError:
        return {"actions": [], "error": "Model returned invalid JSON."}


def process_command(command: str):

    plan = get_plan(command)

    actions = plan.get("actions", [])
    MAX_ACTIONS = 10

    if len(actions) > MAX_ACTIONS:
        return {
            "success": False,
            "message": f"Plan contains too many actions ({len(actions)}).",
        }

    if not actions:
        return {
            "success": False,
            "message": plan.get("error", "No actions were generated."),
        }

    results = []

    for action in actions:

        tool_name = action.get("tool")
        arguments = action.get("arguments", {})

        if not tool_name:
            results.append(
                {"success": False, "message": "Action is missing a tool name."}
            )
            continue

        result = execute_tool(tool_name, arguments)

        results.append({"tool": tool_name, "arguments": arguments, "result": result})

    return {"success": True, "actions_executed": len(results), "results": results}
