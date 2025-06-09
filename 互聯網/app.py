from flask import Flask, render_template, jsonify, request
from model.apnea_model import predict_apnea
import requests
import threading
import time

app = Flask(__name__)

PULSOID_TOKEN = "98a0b9a9-0b8c-41de-acfa-51d9b3650b64"
PULSOID_URL = "https://dev.pulsoid.net/api/v1/data/heart_rate/latest"
HEADERS = {
    "Authorization": f"Bearer {PULSOID_TOKEN}",
    "Content-Type": "application/json"
}

current_heart_rate = "--"
apnea_status = '未知'

def fetch_heart_rate_loop():
    global current_heart_rate
    while True:
        try:
            res = requests.get(PULSOID_URL, headers=HEADERS)
            if res.status_code == 200:
                data = res.json()
                current_heart_rate = data["data"]["heart_rate"]
            else:
                current_heart_rate = "❌ 無法取得"
        except Exception as e:
            current_heart_rate = f"錯誤: {e}"
        time.sleep(0.1)

threading.Thread(target=fetch_heart_rate_loop, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/update_heart_rate", methods=["POST"])
def update_heart_rate():
    global current_heart_rate, apnea_status
    apnea_status = predict_apnea(current_heart_rate)
    return jsonify({"status": "success"})

@app.route("/get_status")
def get_status():
    return jsonify({
        "heart_rate": current_heart_rate,
        "apnea_status": apnea_status
    })

if __name__ == "__main__":
    app.run(debug=True)
