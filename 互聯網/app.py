from flask import Flask, render_template, jsonify, request
from model.apnea_model import predict_apnea

app = Flask(__name__)

current_heart_rate = 75
apnea_status = "未知"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/update_heart_rate", methods=["POST"])
def update_heart_rate():
    global current_heart_rate, apnea_status
    # 由以下這部分接收資料
    data = request.json
    current_heart_rate = data.get("heart_rate", 75) # 測試用
    apnea_status = predict_apnea(current_heart_rate)
    # ###
    return jsonify({"status": "success"})

@app.route("/get_status")
def get_status():
    return jsonify({
        "heart_rate": current_heart_rate,
        "apnea_status": apnea_status
    })

if __name__ == "__main__":
    app.run(debug=True)