from fastapi import FastAPI, Request
import requests

app = FastAPI()



from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()



VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "myverifytoken")  # fallback if not set
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")               # must set in Railway
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")     



@app.get("/")
def home():
    return {"status": "running"}

@app.get("/webhook")
def verify_webhook(request: Request):
    params = request.query_params
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))
    return "Invalid token"

@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        text = message["text"]["body"]

        send_reply(text, sender)

    except Exception as e:
        print("Error:", e)

    return {"status": "success"}

def send_reply(text, sender):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": sender,
        "text": {"body": f"AI Reply: You said — {text}"}
    }

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers)
    print("Response:", r.text)


