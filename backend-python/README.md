# Python Backend

The backend runs as a persistent process, communicating with Electron via JSON over stdin/stdout.

## Modules

| File | Purpose |
|------|---------|
| `main.py` | IPC command router — reads JSON from stdin, dispatches to modules |
| `adb_operations.py` | ADB device info, package listing, uninstall, reinstall |
| `ai_advisor.py` | Perplexity/OpenAI integration for package analysis and chat |
| `openclaw_integration.py` | Natural language command parsing and action execution |
| `backup_manager.py` | Create, list, restore, and delete package backups |

## Setup

```bash
python -m venv .venv
.venv/Scripts/activate          # Windows
pip install -r requirements.txt
echo PERPLEXITY_API_KEY=your_key > .env
```

## IPC Commands

```json
{"command": "get_device_info", "args": {}}
{"command": "list_packages", "args": {"type": "all"}}
{"command": "uninstall_package", "args": {"packageName": "com.example.app"}}
{"command": "reinstall_package", "args": {"packageName": "com.example.app"}}
{"command": "analyze_package", "args": {"packageName": "com.example.app"}}
{"command": "chat_message", "args": {"message": "hello", "history": []}}
{"command": "parse_chat_command", "args": {"message": "remove facebook"}}
{"command": "execute_action", "args": {"action": {...}}}
```

Response: `{"success": true, "data": ...}` or `{"success": false, "error": "..."}`

## Build

```bash
pip install pyinstaller
pyinstaller backend.spec
```

Output: `build-output/backend/backend.exe` — bundled into the Electron app.
