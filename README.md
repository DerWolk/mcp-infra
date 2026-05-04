# 🏗️ MCP Infrastructure

Eine vollständige **Model Context Protocol (MCP)** Implementierung in Python mit SSE-Transport, die Tools, Resources und Prompts bereitstellt.

## 📋 Überblick

Dieses Projekt implementiert das offizielle MCP-Protokoll von Anthropic und bietet:

- **MCP Server** mit SSE (Server-Sent Events) Transport
- **MCP Client** zum Testen und zur Interaktion
- **11 Tools** für Dateisystem, Datenbank, Web, System und Shell-Operationen
- **Resources** für strukturierten Zugriff auf Daten
- **Prompt Templates** für häufige Aufgaben

## 🚀 Features

### Tools (Funktionen)

#### Dateisystem
- `read_file` - Dateiinhalte lesen
- `write_file` - Dateien schreiben
- `list_directory` - Verzeichnisinhalte auflisten

#### Datenbank
- `query_sqlite` - SELECT-Abfragen ausführen
- `execute_sql` - INSERT/UPDATE/DELETE ausführen
- `list_tables` - Tabellen auflisten

#### Web/API
- `fetch_url` - URLs abrufen
- `http_request` - HTTP-Requests mit Custom-Headers

#### System
- `get_system_info` - System-Informationen (CPU, RAM, Disk)
- `list_processes` - Laufende Prozesse auflisten

#### Shell
- `execute_shell_command` - Shell-Befehle ausführen

### Resources (Datenquellen)

- **file://** - Dateien als Resources
- **db://** - Datenbank-Tabellen als Resources
- **system://** - System-Informationen als Resources

### Prompts (Templates)

- `code_review` - Code-Review-Assistent
- `sql_helper` - SQL-Query-Generator
- `system_diagnostics` - System-Diagnose-Helfer
- `api_integration` - API-Integration-Guide

## 📦 Installation

### 1. Repository klonen und Setup

```bash
cd mcp-infrastructure
python -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Abhängigkeiten

Das Projekt benötigt:
- Python 3.10+
- MCP Python SDK
- aiohttp (für SSE-Server)
- aiosqlite (für Datenbank-Tools)
- httpx (für HTTP-Tools)
- psutil (für System-Tools)

## 🎯 Verwendung

### Server starten

```bash
cd server
python main.py
```

Der Server läuft auf:
- **HTTP**: `http://localhost:8000`
- **SSE Endpoint**: `http://localhost:8000/sse`
- **Messages Endpoint**: `http://localhost:8000/messages`

### Client Demo ausführen

```bash
cd client
python client.py
```

Die Demo zeigt:
1. Verbindung zum Server
2. Auflistung aller Tools, Resources und Prompts
3. Beispiel-Aufrufe von Tools
4. Lesen von Resources
5. Verwendung von Prompts

### Eigenen Client erstellen

```python
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    async with sse_client("http://localhost:8000/sse") as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()

            # List tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # Call a tool
            result = await session.call_tool("get_system_info", {})
            print(f"Result: {result.content}")

            # Read a resource
            resource = await session.read_resource("system://info")
            print(f"Resource: {resource.contents}")

            # Get a prompt
            prompt = await session.get_prompt(
                "code_review",
                {"code": "def hello(): return 'world'"}
            )
            print(f"Prompt: {prompt.messages}")

asyncio.run(main())
```

## 🏗️ Projektstruktur

```
mcp-infrastructure/
├── README.md                 # Diese Datei
├── requirements.txt          # Python-Abhängigkeiten
│
├── server/                   # MCP Server
│   ├── main.py              # Server-Hauptdatei (SSE Transport)
│   ├── tools/               # Tool-Implementierungen
│   │   ├── filesystem.py    # Dateisystem-Tools
│   │   ├── database.py      # Datenbank-Tools
│   │   ├── web.py           # Web/API-Tools
│   │   ├── system.py        # System-Tools
│   │   └── shell.py         # Shell-Tools
│   ├── resources/           # Resource-Provider
│   │   └── providers.py     # File/DB/System Resource Provider
│   └── prompts/             # Prompt-Templates
│       └── templates.py     # Template-Definitionen
│
├── client/                   # MCP Client
│   └── client.py            # Client-Implementierung + Demo
│
└── tests/                    # Tests (TODO)
    └── ...
```

## 🔧 Konfiguration

### Server-Port ändern

In `server/main.py`:

```python
site = web.TCPSite(runner, "localhost", 8000)  # Port hier ändern
```

### Timeout für Shell-Befehle anpassen

In `server/tools/shell.py`:

```python
async def execute_shell_command(command: str, timeout: int = 30):  # Timeout hier
```

## 📡 MCP Protokoll

Dieses Projekt implementiert das offizielle Model Context Protocol (MCP) von Anthropic:

- **Transport**: SSE (Server-Sent Events) über HTTP
- **Capabilities**: Tools, Resources, Prompts
- **SDK**: Verwendet das offizielle `mcp` Python-Paket

### Protokoll-Flow

1. **Client verbindet** sich via SSE zum `/sse` Endpoint
2. **Initialize**: Client sendet Initialisierung
3. **Capabilities**: Server antwortet mit verfügbaren Tools/Resources/Prompts
4. **Requests**: Client kann Tools aufrufen, Resources lesen, Prompts abrufen
5. **Responses**: Server antwortet mit strukturierten Daten

## 🎓 Learning Path

### 1. Grundlagen verstehen
- Lies die [offizielle MCP-Dokumentation](https://modelcontextprotocol.io)
- Verstehe Tools, Resources und Prompts
- Lerne SSE (Server-Sent Events)

### 2. Server erkunden
- Starte den Server und öffne `server/main.py`
- Schaue dir die Tool-Registrierung an (`@app.list_tools()`)
- Verstehe wie Tools aufgerufen werden (`@app.call_tool()`)

### 3. Client ausprobieren
- Führe `client/client.py` aus
- Modifiziere die Demo-Aufrufe
- Erstelle eigene Client-Interaktionen

### 4. Erweitern
- Füge neue Tools hinzu (z.B. E-Mail-Versand)
- Erstelle neue Resources (z.B. Git-Repositories)
- Entwickle neue Prompt-Templates

## 🔐 Sicherheitshinweise

⚠️ **WICHTIG**: Dieses Projekt ist für **Learning/Experimentieren** gedacht!

### Produktions-Überlegungen:

1. **Shell-Befehle**: `execute_shell_command` kann **beliebige** Befehle ausführen
   - Implementiere Whitelisting/Sandboxing
   - Validiere Input streng

2. **Dateisystem-Zugriff**: Tools haben Zugriff auf das gesamte Dateisystem
   - Beschränke auf bestimmte Verzeichnisse
   - Implementiere Permissions

3. **Datenbank-Zugriff**: SQL-Injection-Gefahr
   - Verwende Prepared Statements
   - Validiere Queries

4. **HTTP-Requests**: SSRF-Gefahr (Server-Side Request Forgery)
   - Blocke interne IPs
   - Implementiere Rate-Limiting

5. **Authentication**: Aktuell keine Authentifizierung
   - Füge API-Keys hinzu
   - Implementiere OAuth/JWT

## 🧪 Testing

### Tools testen

```bash
# Server starten
cd server && python main.py

# In anderem Terminal: Client ausführen
cd client && python client.py
```

### Einzelne Tools testen

```python
from server.tools.filesystem import read_file
import asyncio

result = asyncio.run(read_file("README.md"))
print(result)
```

## 🛠️ Entwicklung

### Neue Tools hinzufügen

1. Erstelle Funktion in `server/tools/`
2. Registriere in `server/main.py` bei `@app.list_tools()`
3. Handle in `@app.call_tool()`

Beispiel:

```python
# In server/tools/email.py
async def send_email(to: str, subject: str, body: str):
    # Implementation
    return {"success": True}

# In server/main.py
@app.list_tools()
async def list_tools():
    return [
        # ... existing tools
        types.Tool(
            name="send_email",
            description="Send an email",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"}
                },
                "required": ["to", "subject", "body"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any):
    if name == "send_email":
        result = await send_email(
            arguments["to"],
            arguments["subject"],
            arguments["body"]
        )
    # ... handle other tools
```

## 📚 Ressourcen

- [MCP Specification](https://spec.modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [SSE Protocol](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [aiohttp Documentation](https://docs.aiohttp.org)

## 🤝 Beiträge

Dieses Projekt ist ein Learning-Projekt. Fühle dich frei:
- Issues zu erstellen
- Pull Requests einzureichen
- Verbesserungen vorzuschlagen

## 📝 Lizenz

MIT License - Frei verwendbar für Learning und Experimente

## 🎯 Roadmap

- [ ] Unit Tests hinzufügen
- [ ] WebSocket-Transport implementieren
- [ ] Authentication/Authorization
- [ ] Docker-Container
- [ ] Mehr Tools (Git, Docker, etc.)
- [ ] Web-UI für Testing
- [ ] Logging und Monitoring
- [ ] Rate Limiting
- [ ] Input Validation/Sanitization

## 💡 Beispiele

### Beispiel 1: Datei lesen und analysieren

```python
# Mit Client
result = await session.call_tool("read_file", {"path": "data.txt"})
# Dann verwende ein Prompt
prompt = await session.get_prompt("code_review", {"code": result.content[0].text})
```

### Beispiel 2: Datenbank abfragen

```python
# Tabellen auflisten
tables = await session.call_tool("list_tables", {"db_path": "app.db"})

# Query ausführen
result = await session.call_tool("query_sqlite", {
    "db_path": "app.db",
    "query": "SELECT * FROM users LIMIT 10"
})
```

### Beispiel 3: System-Diagnose

```python
# System-Info abrufen
info = await session.call_tool("get_system_info", {})

# Mit Diagnostics-Prompt kombinieren
prompt = await session.get_prompt("system_diagnostics", {
    "issue": f"High memory usage: {info.content[0].text}"
})
```

## 🆘 Troubleshooting

### Server startet nicht
- Prüfe ob Port 8000 frei ist: `lsof -i :8000`
- Ändere Port in `main.py`

### Client kann nicht verbinden
- Stelle sicher, dass Server läuft
- Prüfe URL: `http://localhost:8000/sse`
- Überprüfe Firewall-Einstellungen

### Tools funktionieren nicht
- Prüfe Logs im Server
- Validiere Input-Parameter
- Teste Tools direkt (siehe Testing)

---

**Happy MCP Learning! 🎉**

Bei Fragen oder Problemen, erstelle ein Issue im Repository.
