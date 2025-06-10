import numpy as np
import torch.nn as nn
import torch
from collections import deque

model = torch.jit.load("./model/result/model_scripted_fold2.pt")
model.eval()

hr_window = deque(maxlen=90)

def predict_apnea(hr):
    hr_window.append(hr)

    if len(hr_window) < 90:
        return f"📡 收集中... ({len(hr_window)}/90)"

    # 正規化（與訓練時一致）
    hr_array = np.array(hr_window)
    hr_array = (hr_array - np.mean(hr_array)) / (np.std(hr_array) + 1e-8)

    print(hr_array)

    # 模型輸入格式：(1, 1, 90)
    x = torch.tensor(hr_array, dtype=torch.float32).view(1, 1, 90).to(next(model.parameters()).device)
    with torch.no_grad():
        score = model(x).item()

    # 預測結果
    if score > 0.5:
        return f"⚠️ 有呼吸中止風險 (score={score:.2f})"
    else:
        return f"✅ 正常 (score={score:.2f})"