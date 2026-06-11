# 🚀 Quick Start Guide

Schnelle Anleitung zum Starten der MCP-Infrastruktur.

> **💡 Hinweis:** Diese Anleitung verwendet **stdio Transport** (empfohlen).
> Für SSE-Transport siehe [README_TRANSPORT.md](README_TRANSPORT.md)

## ⚡ 5-Minuten-Setup

### 1. Voraussetzungen prüfen

```bash
# Python-Version prüfen (muss 3.10+ sein)
python3 --version

# Wenn < 3.10, installiere eine neuere Version:
# macOS:
brew install python@3.12

# Ubuntu/Debian:
sudo apt install python3.12

# Windows: Download von python.org
```

### 2. Installation

```bash
# Clone oder navigiere ins Projektverzeichnis
cd mcp-infrastructure

# Virtual Environment erstellen mit Python 3.10+
# macOS/Linux:
python3.12 -m venv venv    # oder python3.11, python3.10
source venv/bin/activate

# Windows:
python -m venv venv
venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt
```

### 3. Client starten (startet Server automatisch)

```bash
# Mit stdio (empfohlen)
cd client
python client_stdio.py

# ODER: Mit SSE (experimentell)
# Terminal 1:
cd server
python main.py

# Terminal 2:
cd client
python client.py
```

Der **stdio-Client** startet den Server automatisch - kein separater Start nötig! 🎉

## ✅ Erfolg prüfen

Wenn alles funktioniert, siehst du:

```
🚀 MCP Client Demo (stdio)

✅ Connected to MCP server

====================================
📦 Available Tools (11):
  • read_file: Read content from a file
  • write_file: Write content to a file
  • list_directory: List contents of a directory
  ...

====================================
📚 Available Resources (2):
  • README (file://README.md)
  • System Information (system://info)

====================================
💬 Available Prompts (4):
  • code_review: Review Python code for best practices
  ...
```

## 🎯 Erste Schritte

### Tool aufrufen

```python
# Mit stdio Transport
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["../server/main_stdio.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # System-Info abrufen
            result = await session.call_tool("get_system_info", {})
            print(result.content[0].text)

asyncio.run(main())
```

### Resource lesen

```python
# System-Info als Resource
resource = await session.read_resource("system://info")
print(resource.contents[0].text)
```

### Prompt verwenden

```python
# Code-Review Prompt
prompt = await session.get_prompt(
    "code_review",
    {"code": "def hello(): return 'world'"}
)
print(prompt.messages[0].content.text)
```

## 🐛 Troubleshooting

### "mcp>=1.0.0 not found"
- **Problem:** Pip zu alt oder Python < 3.10
- **Lösung:**
  ```bash
  pip install --upgrade pip
  python3 --version  # Muss 3.10+ sein
  # Venv neu erstellen mit Python 3.10+
  rm -rf venv
  python3.12 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

### "Server connection error"
- **Problem:** Server kann nicht gestartet werden
- **Lösung:**
  ```bash
  # Prüfe Server-Pfad in client_stdio.py
  # Stelle sicher, dass main_stdio.py existiert
  ls server/main_stdio.py
  ```

### "Import Error: No module named 'aiofiles'"
- **Problem:** Dependencies nicht vollständig installiert
- **Lösung:**
  ```bash
  pip install -r requirements.txt
  ```

## 📚 Nächste Schritte

1. **Lies die README.md** für detaillierte Dokumentation
2. **Schaue dir `client/client_stdio.py`** an für Code-Beispiele
3. **Modifiziere Tools** in `server/tools/`
4. **Erstelle eigene Prompts** in `server/prompts/templates.py`
5. **Lies README_TRANSPORT.md** für Transport-Optionen (stdio vs SSE)

## 🔗 Wichtige Dateien

- **Server (stdio):** `server/main_stdio.py`
- **Server (SSE):** `server/main.py` (experimentell)
- **Client (stdio):** `client/client_stdio.py`
- **Client (SSE):** `client/client.py` (experimentell)

## 💡 Tipps

- **Logs:** Server-Output zeigt alle Requests
- **Debug:** Füge `print()` Statements in Tools hinzu
- **Testing:** Nutze `client.py` als Testumgebung
- **Hot-Reload:** Server muss nach Code-Änderungen neu gestartet werden

---

**Happy Coding! 🎉**

Bei Problemen siehe [README.md](README.md) für ausführliche Dokumentation.
