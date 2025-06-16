# MCP SMTP Email Server 

A secure, bearer-authenticated email tool designed for use within the 365-SACU infrastructure. 
This project exposes a simple FastAPI server with integrated MCP tooling, allowing it to be used with OpenWebUI, 
Claude Desktop, or CLI for dynamic email generation.

---

## Features

- **FastAPI server** with bearer token authentication
- **MCP Tool support** for OpenWebUI integration
- **/send_email endpoint** for dynamic mail delivery
- **Swagger UI (/docs)** with token-based access

---

## Files

| File                  | Purpose                                                |
| ---------------------| ------------------------------------------------------ |
| `main.py`            | Launches FastAPI app, loads MCP tools, exposes routes |
| `mcp_email.py`       | Defines `send_email` tool logic + schema               |
| `config.py`          | Stores the bearer token and email credentials         |

---

## Requirements

- Python 3.11+
- SMTP server access (e.g., Office365, Gmail, Mailjet)
- MCP environment: [mcpo](https://github.com/jmorganca/mcpo)
- Dependencies: `fastapi`, `pydantic`, `smtplib`, `email`, `uvicorn`

---

## Setup

### 1. Clone & Install

```bash
git clone https://github.com/yourname/365-sacu-email-server
cd 365-sacu-email-server
uv pip install -r requirements.txt
```

### 2. Configure

Edit `config.py`:

```python
MCP_BEARER_TOKEN = "your-secret-token"
SMTP_SERVER = "smtp.office365.com" # i used office 365 for my SMTP, I know M$ Graph exists but that is besides the point. If it truly is better than SMTP let me know...
SMTP_PORT = 587
FROM_ADDRESS = "bot@sacu365.org"
SMTP_USERNAME = "bot@sacu365.org"
SMTP_PASSWORD = "your-email-password"
```

### 3. Run

```bash
uvicorn main:app --host 0.0.0.0 --port 8020
```

Then visit: [http://localhost:8020/docs](http://localhost:8020/docs)

---

## Endpoint

### POST `/send_email`

```json
{
  "to": "you@domain.com",
  "subject": "Test Email",
  "body": "Hello from MCP Email Server"
}
```

This tool sends an email using your configured SMTP settings.

---

## MCP Integration

To register this tool in OpenWebUI:

```
URL: http://<host>:8020/openapi.json
Auth: Bearer <your-token>
```

Then call:

```python
await send_email({"to": ..., "subject": ..., "body": ...})
```

---

## Architecture

- MCP tools registered with `@mcp.tool()`
- `send_email` function reads credentials from config and sends via `smtplib`
- FastAPI wraps it in a secure route with token enforcement
- Swagger UI auto-generates schema for OpenWebUI usage

---

## License

MIT. Use freely within your own infrastructure or projects.
