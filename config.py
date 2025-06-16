MAIL_SERVER = "smtp.office365.com"  # Your SMTP server address, i used Office 365 & Zoho SMTP - M$ Graph works too.
MAIL_PORT = 587  # Port for the SMTP server (587 for TLS)
MAIL_USE_TLS = True  # Use TLS for secure connection
MAIL_USE_SSL = False  # Use SSL for secure connection
MAIL_DEFAULT_SENDER = "" # Use your preferred default sender
MAIL_USERNAME = "" # your logon
MAIL_PASSWORD = "" #your logon Pass
MCP_BEARER_TOKEN = "" #If you're not using a token management system (like OAuth2/JWT), you can define your own static token in here and validate it manually! (probably dont do that in prod)
