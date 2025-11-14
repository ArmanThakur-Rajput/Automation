from fastapi import FastAPI, Request
import requests

app = FastAPI()



from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# Load env variables (change as needed)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "myverifytoken")
WHATSAPP_TOKEN = os.getenv("EAAgnK1JElHcBP2NQHQ0vZCiPXdKULk8fSAUCWZCmbE6yZCzp8bgLuRvDkcDH43NOkhNJ9WZCvlROh1q6ZCQsAWMjeDhKK3BVdvq8Tb4rnprXeek6cQcGZCLZBWvy0NXcn80kLrMHKIycnoP3q10D5BGRuCTuv2HgPkZAb2nPxv49rSb0vz9UyOZA4aAFr1ukQSoGCXz8oOB3uXtyscqtt8mwIYOyAVZB2fBPZBNMKxrtHiVZAndopQZDZD")
PHONE_NUMBER_ID = os.getenv("792017460671468")

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

