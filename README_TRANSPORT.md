# 🔌 MCP Transport-Optionen

Dieses Projekt bietet **zwei Transport-Methoden** für die MCP-Kommunikation:

## 1. 📟 stdio Transport (Empfohlen)

**Der Standard-Weg für MCP-Server.**

### Vorteile:
- ✅ Einfach und zuverlässig
- ✅ Standard für MCP-Protokoll
- ✅ Direkte Prozess-zu-Prozess-Kommunikation
- ✅ Keine HTTP-Konfiguration nötig

### Verwendung:

**Server starten:**
```bash
cd server
python main_stdio.py
```

**Client verwenden:**
```bash
cd client
python client_stdio.py
```

### Integration in eigene Apps:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["path/to/server/main_stdio.py"],
    env=None
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        # Nutze den Server...
```

---

## 2. 🌐 SSE Transport (HTTP)

**HTTP-basierte Kommunikation mit Server-Sent Events.**

### Hinweis:
Die SSE-Implementation in `main.py` hat derzeit **Kompatibilitätsprobleme** mit dem MCP Python SDK.

### Status:
- ⚠️ In Entwicklung
- 💡 Für HTTP-basierte Szenarien (z.B. Browser-Clients)
- 🔄 Alternative: Verwende stdio + Reverse Proxy

### Verwendung (wenn funktionsfähig):

**Server starten:**
```bash
cd server
python main.py  # Port 8000
```

**Client verwenden:**
```bash
cd client
python client.py
```

---

## 🎯 Welchen Transport soll ich verwenden?

| Use Case | Empfehlung |
|----------|-----------|
| **Lokale MCP-Server** | ✅ **stdio** |
| **Desktop-Anwendungen** | ✅ **stdio** |
| **Claude Desktop Integration** | ✅ **stdio** |
| **CLI-Tools** | ✅ **stdio** |
| **Web-Anwendungen** | 🔄 stdio + Proxy oder warte auf SSE-Fix |
| **Browser-Clients** | 🔄 stdio + WebSocket-Wrapper |
| **Remote-Server** | 🔄 stdio über SSH oder warte auf SSE-Fix |

---

## 📊 Vergleich

| Feature | stdio | SSE (HTTP) |
|---------|-------|------------|
| **Komplexität** | Niedrig | Mittel |
| **Setup** | Einfach | Konfiguration nötig |
| **Performance** | Schnell | Gut |
| **Netzwerk** | Lokal only | Remote möglich |
| **Browser** | ❌ | ✅ (wenn fertig) |
| **Standard** | ✅ | Alternative |
| **Status** | ✅ Produktiv | ⚠️ In Entwicklung |

---

## 🚀 Quick Start (stdio)

```bash
# Terminal 1: Client starten (startet Server automatisch)
cd /Users/wowa/workspace/MCP/mcp-infrastructure
source venv/bin/activate
cd client
python client_stdio.py
```

Das war's! Der Client startet den Server automatisch über stdio.

---

## 🔧 SSE-Server reparieren (TODO)

Die SSE-Implementation muss angepasst werden, um mit dem MCP SDK kompatibel zu sein.

**Optionen:**
1. **FastAPI/Starlette** statt aiohttp verwenden
2. **Custom SSE-Handler** implementieren
3. **stdio über HTTP-Wrapper** (Reverse Proxy)

Für Production: **Verwende stdio** - es ist der Standard und funktioniert zuverlässig!

---

## 📚 Weitere Informationen

- [MCP Specification](https://spec.modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [SSE Protocol](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
