import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi

from mcp.server.fastmcp import FastMCP
from mcp_email import send_email_tool, EmailInput
from config import *

# === Auth Setup
security = HTTPBearer()

def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != MCP_BEARER_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

# === FastAPI Main App
app = FastAPI(
    title="365-sacu-email-server",
    version="1.2.9",
    description="Email tool secured via Basic Auth. Originally written by Nelson Orellana on 06.16.2025.",
)

# === MCP Server
mcp = FastMCP("365-email-server")
#send_email(mcp)  # register @mcp.tool()
send_email = send_email_tool(mcp)  # get reference to the function

@app.post("/send_email", tags=["MCP Tools"], dependencies=[Depends(verify_bearer_token)])
async def send_email_route(data: EmailInput):
    return await send_email(data)  # this works now because of send_email

# === Mount the MCP-generated FastAPI router directly
# This copies MCP tools into the main app's route space
for route in mcp.streamable_http_app().routes:
    app.router.routes.append(route)


# === Secure all routes with Basic Auth
@app.middleware("http")
async def enforce_basic_auth(request, call_next):
    if request.url.path in ["/openapi.json", "/docs", "/docs/oauth2-redirect"]:
        return await call_next(request)  # allow OpenWebUI to access docs
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth.split("Bearer ")[1].strip()
    if token != MCP_BEARER_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await call_next(request)

# === Swagger Auth Button (already auto-included if HTTPBasic is used via Depends)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema.setdefault("components", {})["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer"
        }
    }
    schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi
