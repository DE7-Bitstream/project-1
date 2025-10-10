const bar_labels = JSON.parse(document.getElementById("top5SongName").textContent);
const bar_data = JSON.parse(document.getElementById("top5ChartInCount").textContent);
const line_labels = JSON.parse(document.getElementById("top5RankLabels").textContent);
const line_data = JSON.parse(document.getElementById("top5Rank").textContent);

const ctx_1 = document.getElementById('top5BarChart').getContext('2d');
const top5BarChart = new Chart(ctx_1, {
    type: 'bar',
    data: {
        labels: bar_labels,
        datasets: [{
            label: '차트 진입 횟수',
            data: bar_data,
            backgroundColor : [
                'rgba(255, 255, 153, 0.75)',
                'rgba(152, 255, 152, 0.75)',
                'rgba(173, 216, 230, 0.75)',
                'rgba(221, 160, 221, 0.75)',
                'rgba(255, 192, 203, 0.75)',
            ]
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});

const ctx_2 = document.getElementById('top5LineChart').getContext('2d');
const top5LineChart = new Chart(ctx_2, {
    type : 'line',
    data : {
        labels : line_labels,
        datasets : line_data,
    },
    options : {
        scales : {
            y : {
                beginAtZero: true,
                reverse : true,
                min : 1,
                max : 100,
            }
        }
    }
})