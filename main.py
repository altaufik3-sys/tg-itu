from flask import Flask, request
import requests
import csv
import io

TOKEN = "8231384008:AAEM2j6MqYm_UZ8lwlh781WmPq-TAI-PqxY"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1ioBVMt0rAlxZ5DdiXaDNXikRgPzJleD9NIMfV_Oy-VU/export?format=csv"
WEBHOOK_URL = "https://NAMA-APP-KAMU.onrender.com"  # ubah nanti sesuai URL Render kamu

app = Flask(__name__)

def get_sheet_data():
    res = requests.get(SHEET_CSV_URL)
    res.encoding = 'utf-8'
    data = list(csv.reader(io.StringIO(res.text)))
    headers = data[3]
    rows = data[4:]
    return headers, rows

@app.route('/')
def home():
    return "✅ Bot is running."

@app.route(f'/{TOKEN}', methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    if not update or 'message' not in update:
        return 'no message'

    chat_id = update['message']['chat']['id']
    text = update['message'].get('text', '').strip()

    if text == '/start':
        send_message(chat_id, "Halo 👋\nKirim kode unit seperti `T355` untuk melihat data service.", True)
        return 'ok'

    headers, rows = get_sheet_data()
    try:
        unit_index = headers.index('Unit')
    except ValueError:
        send_message(chat_id, "⚠️ Kolom 'Unit' tidak ditemukan.", True)
        return 'ok'

    found = next((r for r in rows if r[unit_index].strip() == text), None)
    if found:
        def val(col): 
            return found[headers.index(col)] if col in headers else "-"
        reply = (
            f"🔧 *Data Service Unit {text}*\n\n"
            f"🗓 Last Service: {val('Last Service')}\n"
            f"⏱ Last Interval: {val('Last Inter')}\n"
            f"⚙️ HM Now: {val('HM Now')}\n"
            f"📅 Next Service: {val('Next Service')}\n"
            f"⌛ Lifetime: {val('Lifetime')}"
        )
    else:
        reply = "❌ Unit tidak ditemukan. Coba cek kembali."

    send_message(chat_id, reply, True)
    return 'ok'

def send_message(chat_id, text, markdown=False):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    if markdown:
        payload['parse_mode'] = 'Markdown'
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

