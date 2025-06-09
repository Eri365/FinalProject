async function fetchStatus() {
    try {
        const response = await fetch("/get_status");
        const data = await response.json();

        // 更新心跳
        document.getElementById("heartRate").innerText = `${data.heart_rate} bpm`;

        // 更新狀態文字與樣式
        const statusElement = document.getElementById("apneaStatus");
        statusElement.innerText = data.apnea_status;

        if (data.apnea_status.includes("正常")) {
            statusElement.className = "h4 status-good";
        } else if (data.apnea_status.includes("中止")) {
            statusElement.className = "h4 status-bad";
        } else {
            statusElement.className = "h4 text-secondary";
        }
    } catch (error) {
        console.error("取得狀態時發生錯誤：", error);
    }
}

// 每 2 秒更新一次畫面
setInterval(fetchStatus, 2000);

// 初始化時也先抓一次
fetchStatus();