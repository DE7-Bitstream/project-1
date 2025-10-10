const top3Song = JSON.parse(document.getElementById("top3Song").textContent);
const bar_labels = top3Song.map(item => item[0]);
const bar_data = top3Song.map(item => item[1]);

const bar = document.getElementById('top3SongBarChart').getContext('2d');
const top3SongBarChart = new Chart(bar, {
    type: 'bar',
    data: {
        labels: bar_labels,
        datasets: [{
            label: '차트 진입 횟수',
            data: bar_data,
            backgroundColor : [
                'rgba(255, 153, 51, 0.6)',
                'rgba(51, 175, 255, 0.6)',
                'rgba(102, 204, 102, 0.6)'
            ]
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});

document.getElementById('select_genre').addEventListener('change', async function() {
    const selectedGenre = this.value;
    const response = await fetch(`?ajax=1&genre=${encodeURIComponent(selectedGenre)}`);
    const data = await response.json();
    const top3Song = data.top3_songs;

    const top3Container = document.querySelector('.top3_song');
    top3Container.innerHTML = '';
    top3Song.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'top_song';
        div.innerHTML = `
            <a class="rank">${index + 1}</a>
            <img src="https://placehold.co/200x200" width="150" height="150" alt="${index + 1}">
            <a class='song_name'>${item[0]}</a>
            <a class='song_count'>차트 진입 : ${item[1]}회</a>
        `;
        top3Container.appendChild(div);
    });

    top3SongBarChart.data.labels = top3Song.map(item => item[0]);
    top3SongBarChart.data.datasets[0].data = top3Song.map(item => item[1]);
    top3SongBarChart.update();

    // 3. 앨범 제목 업데이트
    document.getElementById('album_title').textContent = `${selectedGenre} TOP 3`;
})