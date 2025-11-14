from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# Load environment variables safely
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "myverifytoken")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# Check env vars on startup
if not WHATSAPP_TOKEN:
    print("WARNING: WHATSAPP_TOKEN not set!")
if not PHONE_NUMBER_ID:
    print("WARNING: PHONE_NUMBER_ID not set!")

@app.get("/")
def health_check():
    """
    Health check route to confirm the app is running
    """
    return {"status": "running"}

@app.get("/webhook")
def verify_webhook(request: Request):
    """
    Verify webhook for WhatsApp
    """
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        # Return challenge without int() to avoid type errors
        return challenge or "0"
    return {"status": "failed", "reason": "Invalid verify token"}

@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Receive incoming WhatsApp messages and reply
    """
