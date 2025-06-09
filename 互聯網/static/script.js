const heartRateElem = document.getElementById("heartRate");
const apneaStatusElem = document.getElementById("apneaStatus");

const ctx = document.getElementById("heartRateChart").getContext("2d");
let heartRateData = [];
let timeLabels = [];

const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: timeLabels,
        datasets: [{
            label: '心跳（bpm）',
            data: heartRateData,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            tension: 0.4,
            fill: true
        }]
    },
    options: {
        responsive: true,
        animation: false,
        scales: {
            y: {
                min: 40,
                max: 160
            }
        },
        plugins: {
            legend: {
                display: true
            }
        }
    }
});

function updateStatus() {
    fetch("/get_status")
        .then(res => res.json())
        .then(data => {
            const heartRate = data.heart_rate;
            const status = data.apnea_status;

            // 更新文字顯示
            heartRateElem.textContent = `${heartRate} bpm`;
            apneaStatusElem.textContent = status;
            apneaStatusElem.className = (status === "Yes")
                ? "h4 status-bad"
                : "h4 status-good";

            // 更新折線圖
            const now = new Date();
            const label = now.toLocaleTimeString();

            if (!isNaN(heartRate)) {
                timeLabels.push(label);
                heartRateData.push(heartRate);

                if (timeLabels.length > 30) {
                    timeLabels.shift();
                    heartRateData.shift();
                }

                chart.update();
            }
        });
}

setInterval(updateStatus, 1000);