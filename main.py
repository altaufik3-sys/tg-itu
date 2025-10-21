from flask import Flask, request
import requests
import gspread

app = Flask(__name__)

TELEGRAM_TOKEN = "8231384008:AAEM2j6MqYm_UZ8lwlh781WmPq-TAI-PqxY"
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# Hubungkan ke Google Sheet (tanpa OAuth)
# Gunakan link publik CSV dari Sheet
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1ioBVMt0rAlxZ5DdiXaDNXikRgPzJleD9NIMfV_Oy-VU/export?format=csv"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "").strip()

        if text.startswith("/start"):
            send(chat_id, "Halo! Ketik nama unit (misal: T344)")
        else:
            send(chat_id, f"Kamu mengetik: {text}")

    return {"ok": True}

def send(chat_id, text):
    requests.post(TELEGRAM_URL, json={"chat_id": chat_id, "text": text})

@app.route("/", methods=["GET"])
def index():
    return "Bot aktif!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  
