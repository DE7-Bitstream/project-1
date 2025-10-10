const pie_labels = JSON.parse(document.getElementById("top5Genre").textContent);
const pie_data = JSON.parse(document.getElementById("top5GenreCount").textContent);

const pie = document.getElementById('top5GenrePie').getContext('2d');
const top5GenrePie = new Chart(pie, {
    type : 'pie',
    data : {
        labels : pie_labels,
        datasets : [{
            label : '차트 진입 횟수',
            data : pie_data,
            backgroundColor : [
                'rgba(255, 205, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(153, 102, 255, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 255, 255, 0)'
            ],
            hoverOffset : 100
        }]
    }
})