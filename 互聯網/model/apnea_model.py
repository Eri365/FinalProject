def predict_apnea(hr):
    # 簡單模擬：過低的心跳可能代表呼吸中止
    if hr < 50:
        return "可能有睡眠呼吸中止症"
    else:
        return "狀態正常"