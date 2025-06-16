from email.message import EmailMessage
import smtplib
import json
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
from config import *

# Email settings
SMTP_SERVER = MAIL_SERVER
SMTP_PORT = MAIL_PORT
SMTP_USERNAME = MAIL_USERNAME
SMTP_PASSWORD = MAIL_PASSWORD
FROM_ADDRESS = SMTP_USERNAME

# Tool input model
class EmailInput(BaseModel):
    to: str
    subject: str
    body: str

# Register tool with a given FastMCP instance
def send_email_tool(mcp: FastMCP):
    @mcp.tool()
    async def send_email(data: EmailInput) -> str:
        try:
            msg = EmailMessage()
            msg["From"] = FROM_ADDRESS
            msg["To"] = data.to
            msg["Subject"] = data.subject
            msg.set_content(data.body)

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)

            return json.dumps({"status": "Email sent"})
        except Exception as e:
            return json.dumps({"error": str(e)}), 500

    return send_email
